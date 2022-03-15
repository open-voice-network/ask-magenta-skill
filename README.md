# Ask Magenta

Magenta Voice Platform interoperability enabler.

## About

The skill connects Mycroft speaker to Magenta Voice Platform.  

As Magenta Voice Platform supports German language only, the skill auto-translates user queries from English to German,
and Platform answers - from German back to English.

## Usage

To ask a single question: _**"Hey Mycroft, ask Magenta <question>"**_, e.g: **_"Hey Mycroft, ask Magenta the weather in London"_**  

To activate Magenta: **_"Hey Mycroft, launch Magenta"_**. After the launch, all user queries will be sent to Magenta Platform.

To stop Magenta: **_"Hey Mycroft, terminate Magenta"_**.

## Configuration

Skill requires the following environment variables to operate:

- **ENVIRONMENT**: Magenta Voice target environment  
- **TENANT**: Magenta Voice tenant
- **API_KEY**: API key to connect to the tenant
- **BASE_URL**: base URL of the Magenta Voice Platform API 
- **USER_API**: URL path to user management API
- **INVOKE_TEXT**: URL path to send text API
- **TESTING_SECRET**: API token encoding secret 


## Mycroft STT/TTS in German

Here is the configuration to run STT/TTS in German:

STT: [Mozilla DeepSpeech](https://github.com/mozilla-services/deepspeech-server) with a model from [Aashish Agarwal](https://github.com/AASHISHAG/deepspeech-german)
TTS: [Google Speech services](https://cloud.google.com/text-to-speech)

```json
{
  "lang": "de-de",
  "max_allowed_core_version": 21.2,
  "stt": {
    "deepspeech_server": {
      "uri": "http://localhost:8080/stt"
    },
    "module": "deepspeech_server"
  },
  "tts": {
    "module": "google",
    "google": {
      "lang": "de"
    }
  }
}
```

> Reference: https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/customizations/languages/german  


## Credits
- Deborah Dahl

- [tvadim](https://github.com/tvadim)

## Category

> **Information**

## Tags
