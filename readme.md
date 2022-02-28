## Description

OVOS TTS plugin for [Mimic2](https://github.com/MycroftAI/mimic2)

## Install

`pip install ovos-tts-plugin-mimic2`

## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic2",
    "ovos-tts-plugin-mimic2": {
        "voice": "kusal"
    }
  }
 
```

### Voices

Available Voices:
- Kusal - Mycroft AI official voice, hosted by Mycroft
- Nancy - trained on [Nancy Corpus](http://www.cstr.ed.ac.uk/projects/blizzard/2011/lessac_blizzard2011/) by [@MXGray](https://github.com/MXGray, hosted by Neon
- ljspeech - trained on [LJ-Speech-Dataset](https://keithito.com/LJ-Speech-Dataset) by [keithito](https://github.com/keithito/tacotron), hosted by Neon

### Self Hosting

The Kusal voice model is not provided by MycroftAI and can not be self hosted

```
docker pull ghcr.io/openvoiceos/mimic2-nancy:dev
docker pull ghcr.io/openvoiceos/mimic2-ljspeech:dev
```

You can also build the containers locally

```
docker build -f nancy.Dockerfile -t mimic2-nancy
docker build -f ljspeech.Dockerfile -t mimic2-ljspeech
```

run the container 

`docker run --rm -p 9000:9000 mimic2-nancy`

set url and voice in config, voice is used for local caching of files by ovos plugins

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic2",
    "ovos-tts-plugin-mimic2": {
        "url": "http://0.0.0.0:9000/synthesize",
        "voice": "nancy"
    }
  }
 
```