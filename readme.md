## Description

OVOS TTS plugin for [Mimic2](https://github.com/MycroftAI/mimic2)

## Install

`pip install ovos-tts-plugin-mimic2`

## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic2",
    "ovos-tts-plugin-mimic2": {
        "url": "https://mimic-api.mycroft.ai/synthesize"
    }
  }
 
```

### Voices

Dockerfiles are provided for Nancy corpus trained by Mxgray and LJSpeech trained by Keithito
- `docker build -f nancy.Dockerfile -t mimic2-nancy`
- `docker build -f ljspeech.Dockerfile -t mimic2-ljspeech`

run the container and set url in config `http://0.0.0.0:9000/synthesize`
- `docker run --rm -p 9000:9000 mimic2-nancy`