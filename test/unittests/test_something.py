# write your first unittest!
import unittest

from ovos_tts_plugin_mimic2 import Mimic2TTSPlugin


class TestTTS(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mimic = Mimic2TTSPlugin()

    def test_something(self):
        path = "/tmp/hello_kusal.wav"
        audio, phonemes = self.mimic.get_tts("hello world", path)
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
