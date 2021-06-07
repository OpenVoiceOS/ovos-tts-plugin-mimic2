from ovos_tts_plugin_mimic2 import Mimic2TTSPlugin

mimic = Mimic2TTSPlugin()
mimic.get_tts("hello world", "cached_server_side.wav")
mimic.get_tts("this is kusal, the mimic2 voice, also known was American "
              "Male", "not_cached.wav")