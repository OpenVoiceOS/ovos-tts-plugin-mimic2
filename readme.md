## Description

OVOS TTS plugin for [Mimic2](https://github.com/MycroftAI/mimic2)

## Install

`pip install ovos-tts-plugin-mimic2`

## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic2",
    "ovos-tts-plugin-mimic2": {
        "url": "https://mimic-api.mycroft.ai"
    }
  }
 
```

### Voices

- kusal - male - default voice by mycroft - https://mimic-api.mycroft.ai/synthesize
- nancy - female - build and run dockerfile - http://localhost:9000/synthesize
    - `docker build . -t mimic2-nancy`
    - `docker run --rm -p 9000:9000 mimic2-nancy`