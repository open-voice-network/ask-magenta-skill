from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util import LOG

from .magenta.voice.client import ApiClient


class AskMagenta(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler("magenta.ask.intent")
    def handle_magenta_ask(self, message: Message):
        LOG.info("Message: %s", repr(message))
        utterance = message.data["utterance"]
        self.speak_dialog("magenta.ask", message.data)
        with ApiClient() as client:
            client.connect()
            response = client.invoke_text(utterance)
            LOG.info("Response: %s", repr(response))
            self.speak_dialog(response.text)


def create_skill():
    return AskMagenta()
