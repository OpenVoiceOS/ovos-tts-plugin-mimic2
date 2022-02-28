# write your first unittest!
import unittest

from ovos_tts_plugin_mimic2 import Mimic2TTSPlugin


class TestTTS(unittest.TestCase):
    def test_kusal(self):
        path = "/tmp/hello_kusal.wav"
        mimic = Mimic2TTSPlugin()
        audio, phonemes = mimic.get_tts("hello world", path)
        self.assertEqual(audio, path)
        self.assertEqual(phonemes,
                         [['HH', '0.0775'],
                          ['AH', '0.1550'],
                          ['L', '0.2325'],
                          ['OW', '0.3100'],
                          ['W', '0.4340'],
                          ['ER', '0.5580'],
                          ['L', '0.6820'],
                          ['D', '0.8060']])

    def test_nancy(self):
        path = "/tmp/hello_nancy.wav"
        mimic = Mimic2TTSPlugin(config={"voice": "nancy"})
        audio, phonemes = mimic.get_tts("hello world", path)
        self.assertEqual(audio, path)
        self.assertEqual(phonemes, None)

    def test_ljspeech(self):
        path = "/tmp/hello_ljspeech.wav"
        mimic = Mimic2TTSPlugin(config={"voice": "ljspeech"})
        audio, phonemes = mimic.get_tts("hello world", path)
        self.assertEqual(audio, path)
        self.assertEqual(phonemes, None)
