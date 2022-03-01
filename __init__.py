from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util import LOG
from adapt.intent import IntentBuilder
from mtranslate import translate

from .magenta.voice.client import ApiClient

LANG = "de"
NO_INTENT = "no.intent"
ASK_MAGENTA = "ask.magenta"


class AskMagenta(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder("AskMagentaIntent").require("AskMagentaKeyword").require("utterance").build())
    def handle_magenta_ask(self, message: Message):
        LOG.info("Message: %s", message.serialize())
        utterance = message.data["utterance"]
        translated = translate(utterance, from_language=self.lang, to_language=LANG)
        self.speak_dialog(ASK_MAGENTA, message.data)
        with ApiClient() as client:
            client.connect()
            LOG.info("Translated: %s", translated)
            response = client.invoke_text(translated)
            LOG.info("Response: %s", repr(response))
            answer = translate(response.text, from_language=LANG, to_language=self.lang) if response.text else NO_INTENT
            LOG.info("Translated answer: %s", answer)
            self.speak_dialog(answer)


def create_skill():
    return AskMagenta()
