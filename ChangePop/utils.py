import re
from mailjet_rest import Client
import os

def api_resp(code, mtype, msg):
    # TODO Doc
    r = {
        "code": str(code),
        "type": str(mtype),
        "message": str(msg)}
    return r


def fix_str(string):
    string = re.sub('[\'(),]', '', string)
    return string

def send_mail():

    api_key = "288ca9ac426b3e41809ee9c8a429a974"
    api_secret = "1f29a950828de1e093e7c8d4b74bd5ab"
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
                    {
                            "From": {
                                    "Email": "info@kalepa.com",
                                    "Name": "Kalepa Info"
                            },
                            "To": [
                                    {
                                            "Email": "javiergimenezgarces@gmail.com",
                                            "Name": "passenger 1"
                                    }
                            ],
                            "Subject": "Your email flight plan!",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!"
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    return result.json()

