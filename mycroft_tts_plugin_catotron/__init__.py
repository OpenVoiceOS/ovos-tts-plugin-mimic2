# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from mycroft.tts import TTS, TTSValidator
import requests
from pydub import AudioSegment
from os.path import join, isfile, isdir
from os import makedirs
import re
import math
from tempfile import gettempdir
from hashlib import sha512


class CatotronTTSPlugin(TTS):
    """Interface to Catotron TTS."""
    # Heuristic value, caps character length of a chunk of text
    # to be spoken as a work around for current Catotron implementation limits.
    max_sentence_size = 150

    def __init__(self, lang="es-ca", config=None):
        super(CatotronTTSPlugin, self).__init__(
            lang, config, CatotronTTSValidator(self), 'wav')
        self.url = config.get("url",
                              "http://catotron.collectivat.cat/synthesize")
        # max size for catotron is 150 chars, sentences will be split at
        # punctuation and merged again, this value defines the silence
        # between merging sound files
        self.pause_between_chunks = config.get("pause_between_chunks", 0.6)
        # cache is used to speed up repeated synths and save api calls
        self.cache = config.get("cache_dir") or join(gettempdir(), "catotron")
        self.cache_enabled = config.get("cache_enabled", True)
        if not self.cache_enabled:
            # used only for intermediate files
            self.cache = join(gettempdir(), "catotron")
        if not isdir(self.cache):
            makedirs(self.cache)

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio using Catotron endpoint.

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        cached_file = self._get_unique_file_path(sentence)
        if isfile(cached_file) and self.cache_enabled:
            with open(cached_file, "rb") as f:
                audio_data = f.read()
            with open(wav_file, "wb") as f:
                f.write(audio_data)
        else:
            if len(sentence) > self.max_sentence_size:
                return self._get_tts_chunked(sentence, wav_file)
            params = {"text": sentence}
            audio_data = requests.get(self.url, params=params).content
            with open(wav_file, "wb") as f:
                f.write(audio_data)
            if self.cache_enabled:
                with open(cached_file, "wb") as f:
                    f.write(audio_data)
        return (wav_file, None)  # No phonemes

    # bellow are helpers to split sentence in chunks that catotron can synth
    # there is a limit for 150 chars
    def _get_tts_chunked(self, sentence, wav_file):
        combined = AudioSegment.empty()
        silence = AudioSegment.silent(duration=self.pause_between_chunks)
        for splitted in self._split_sentences(sentence):
            partial_file = self._get_unique_file_path(splitted)
            if not isfile(partial_file):
                partial_file, _ = self.get_tts(splitted, partial_file)
            combined += silence + AudioSegment.from_wav(partial_file)
        combined.export(wav_file, format="wav")
        return (wav_file, None)  # No phonemes

    def _get_unique_file_path(self, sentence):
        file_name = sha512(sentence.encode('utf-8')).hexdigest()
        return join(self.cache, file_name) + ".wav"

    @staticmethod
    def _split_sentences(text):
        """Split text into smaller chunks for TTS generation.
        NOTE: The smaller chunks are needed due to current Catotron TTS limitations.
        This stage can be removed once Catotron can generate longer sentences.
        Arguments:
            text (str): text to split
            chunk_size (int): size of each chunk
            split_by_punc (bool, optional): Defaults to True.
        Returns:
            list: list of text chunks
        """
        if len(text) <= CatotronTTSPlugin.max_sentence_size:
            return [CatotronTTSPlugin._add_punctuation(text)]

        # first split by punctuations that are major pauses
        first_splits = CatotronTTSPlugin._split_by_punctuation(
            text,
            puncs=[r'\.', r'\!', r'\?', r'\:', r'\;']
        )

        # if chunks are too big, split by minor pauses (comma, hyphen)
        second_splits = []
        for chunk in first_splits:
            if len(chunk) > CatotronTTSPlugin.max_sentence_size:
                second_splits += CatotronTTSPlugin._split_by_punctuation(
                    chunk, puncs=[r'\,', '--', '-'])
            else:
                second_splits.append(chunk)

        # if chunks are still too big, chop into pieces of at most 20 words
        third_splits = []
        for chunk in second_splits:
            if len(chunk) > CatotronTTSPlugin.max_sentence_size:
                third_splits += CatotronTTSPlugin._split_by_chunk_size(
                    chunk, 20)
            else:
                third_splits.append(chunk)

        return [CatotronTTSPlugin._add_punctuation(chunk)
                for chunk in third_splits]

    @staticmethod
    def _break_chunks(l, n):
        """Yield successive n-sized chunks
        Arguments:
            l (list): text (str) to split
            chunk_size (int): chunk size
        """
        for i in range(0, len(l), n):
            yield " ".join(l[i:i + n])

    @staticmethod
    def _split_by_chunk_size(text, chunk_size):
        """Split text into word chunks by chunk_size size
        Arguments:
            text (str): text to split
            chunk_size (int): chunk size
        Returns:
            list: list of text chunks
        """
        text_list = text.split()

        if len(text_list) <= chunk_size:
            return [text]

        if chunk_size < len(text_list) < (chunk_size * 2):
            return list(CatotronTTSPlugin._break_chunks(
                text_list,
                int(math.ceil(len(text_list) / 2))
            ))
        elif (chunk_size * 2) < len(text_list) < (chunk_size * 3):
            return list(CatotronTTSPlugin._break_chunks(
                text_list,
                int(math.ceil(len(text_list) / 3))
            ))
        elif (chunk_size * 3) < len(text_list) < (chunk_size * 4):
            return list(CatotronTTSPlugin._break_chunks(
                text_list,
                int(math.ceil(len(text_list) / 4))
            ))
        else:
            return list(CatotronTTSPlugin._break_chunks(
                text_list,
                int(math.ceil(len(text_list) / 5))
            ))

    @staticmethod
    def _split_by_punctuation(chunks, puncs):
        """Splits text by various punctionations
        e.g. hello, world => [hello, world]
        Arguments:
            chunks (list or str): text (str) to split
            puncs (list): list of punctuations used to split text
        Returns:
            list: list with split text
        """
        if isinstance(chunks, str):
            out = [chunks]
        else:
            out = chunks

        for punc in puncs:
            splits = []
            for t in out:
                # Split text by punctuation, but not embedded punctuation.  E.g.
                # Split:  "Short sentence.  Longer sentence."
                # But not at: "I.B.M." or "3.424", "3,424" or "what's-his-name."
                splits += re.split(r'(?<!\.\S)' + punc + r'\s', t)
            out = splits
        return [t.strip() for t in out]

    @staticmethod
    def _add_punctuation(text):
        """Add punctuation at the end of each chunk.
        Catotron expects some form of punctuation at the end of a sentence.
        """
        punctuation = ['.', '?', '!', ';']
        if len(text) >= 1 and text[-1] not in punctuation:
            return text + ', '
        else:
            return text


class CatotronTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CatotronTTSValidator, self).__init__(tts)

    def validate_lang(self):
        lang = self.tts.lang.lower()
        assert lang in ["ca", "ca-es", "es-ca"]

    def validate_connection(self):
        base_url = self.tts.url.replace("/synthesize", "")
        assert requests.get(base_url).status_code == 200

    def get_tts_class(self):
        return CatotronTTSPlugin
