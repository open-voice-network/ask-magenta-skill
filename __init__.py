from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util import LOG
from adapt.intent import IntentBuilder
from mtranslate import translate

from .magenta.voice.client import ApiClient

LANG = "de"
NO_INTENT = "no.intent"
ASK_MAGENTA = "ask.magenta"
LAUNCH_MAGENTA = "launch.magenta"
STOP_MAGENTA = "stop.magenta"


class AskMagenta(MycroftSkill):

    client: ApiClient

    def __init__(self):
        super().__init__()
        self.client = ApiClient()

    @intent_handler(IntentBuilder("AskMagentaIntent").require("AskMagentaKeyword").require("utterance").build())
    def handle_magenta_ask(self, message: Message):
        """Send a single query to magenta"""
        LOG.info("Message: %s", message.serialize())
        utterance = message.data["utterance"]
        translated = translate(utterance, from_language=self.lang, to_language=LANG)
        self.speak_dialog(ASK_MAGENTA, message.data)
        with ApiClient() as client:
            client.connect()
            response = client.invoke_text(translated)
            LOG.info("Translated: %s", repr(response))
            answer = translate(response.text, from_language=LANG, to_language=self.lang) if response.text else NO_INTENT
            LOG.info("Translated answer: %s", answer)
            self.speak_dialog(answer)

    @intent_handler(IntentBuilder("LaunchMagentaIntent").require("LaunchMagentaKeyword").build())
    def handle_magenta_launch(self, message: Message):
        """Connects Magenta client"""
        LOG.info("Message: %s", message.serialize())
        self.client.connect()
        LOG.info("Connected to: %s", repr(self.client))
        self.speak_dialog(LAUNCH_MAGENTA)

    @intent_handler(IntentBuilder("StopMagentaIntent").require("StopMagentaKeyword").build())
    def handle_magenta_stop(self, message: Message):
        """Disconnects Magenta client"""
        LOG.info("Message: %s", message.serialize())
        self.client.disconnect()
        self.speak_dialog(STOP_MAGENTA)

    def converse(self, message=None):
        """Handles conversation to Magenta"""
        LOG.info("Message: %s", message.serialize())

        try:
            utterance = message.data["utterances"][0]
        except (IndexError, TypeError):
            return False

        if not self.client.is_connected() or self.voc_match(utterance, "StopMagentaKeyword"):
            return False

        translated = translate(utterance, from_language=self.lang, to_language=LANG)
        response = self.client.invoke_text(translated)
        answer = translate(response.text, from_language=LANG, to_language=self.lang) if response.text else NO_INTENT
        self.speak_dialog(answer)

        return True


def create_skill():
    return AskMagenta()
