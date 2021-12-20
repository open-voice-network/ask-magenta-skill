from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.api import Api
import requests
from requests.structures import CaseInsensitiveDict
from mycroft.util import LOG

class AskMagenta(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('magenta.ask.intent')
    def handle_magenta_ask(self, message):
        self.speak_dialog('magenta.ask')
        answer = request_info_from_magenta(message)
        self.speak_dialog(answer)
        
def create_skill():
    return AskMagenta()
    
def request_info_from_magenta(message):
	#first get the access token by logging in
	loginUrl = "https://smartvoicehub.de/"
	headers = CaseInsensitiveDict()
	headers["accept"] = "application/json"
	headers["apikey"] = "redacted"
	headers["Content-Type"] = "application/json"
		
	data = '''
		{
 	   	"accessTokenLifetime": 3600,
 	  	 "authentication": "aaaa-bbbb-cccc-dddddddd",
  	  	"productPayload": {
  	     	 "text": "What is the weather in Darmstadt"
   	 	},
 	 	  "refreshTokenLifetime": 36000,
  	 	 "scopes": [
  	      	"OVON_demo"
  	  	],
  	  	"userId": "BrianCornell"
		}
	'''

	loginResp = requests.post(loginUrl, headers=headers, data=data)
	jsonResp = loginResp.json()
	accessToken = "Bearer " + jsonResp['accessToken']

	#then send the request for interpretation
	#first remove the 'ask magenta' prefix
	LOG.info(message.data['utterances'][0])
	toSend = message.data['utterances'][0]
	toSendFinal = toSend.replace('ask magenta ','')
	
	#construct http POST request
	interpretationUrl = "https://smartvoicehub.de/"
	headers = CaseInsensitiveDict()
	headers["Authorization"] = accessToken
	headers["Content-Type"] = "application/json"
	headers["Accept"] = "application/json"
	headers["apikey"] = "aaaa-bbbb-cccc-dddd"
	dataString = '"text":' + '"' + toSendFinal + '"'
	dataTest = '{' + dataString + '}'
	LOG.info(dataTest)
	
	#send the request
	interpretationResp = requests.post(interpretationUrl, headers=headers, data=dataTest)
	
	#extract Magenta's reply  from the response
	jsonInterpretation = interpretationResp.json()
	answer = jsonInterpretation['text']
	return answer

