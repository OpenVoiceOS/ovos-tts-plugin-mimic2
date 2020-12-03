## Description
Mycroft TTS plugin for [Catotron](http://catotron.collectivat.cat/)

The "plugins" are pip install-able modules presenting one or more entrypoints with a entrypoint group defined in setup.py

more info in the [original PR](https://github.com/MycroftAI/mycroft-core/pull/2594)

## Install

`mycroft-pip install jarbas-tts-plugin-catotron`

## Configuration

```json
  "tts": {
    "module": "catotron_tts_plug"
  }
 
```

### Extra options

max size for catotron is 150 chars, sentences will be split at punctuation and merged again

- url, you can self host catotron https://github.com/CollectivaT-dev/catotron-cpu
- pause_between_chunks defines the silence between merging sound files
- cache_dir is used to save synthesized audio files, this is used to speed up repeated synths and save api calls, if not set a temporary directory will be used
- cache_enabled can be set to false, this will disable the caching of files, intermediate file chunks will still be created in a temporary directory
           
Default values are

```json
  "tts": {
    "module": "catotron_tts_plug",
    "catotron_tts_plug": {
      "url": "http://catotron.collectivat.cat/synthesize",
      "pause_between_chunks": 0.6,
      "cache_dir": "/tmp/catotron",
      "cache_enabled": true
    }
 
```
