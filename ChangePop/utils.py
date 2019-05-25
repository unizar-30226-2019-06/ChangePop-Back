import random
import re
import string

from mailjet_rest import Client
import os

def api_resp(code, mtype, msg):
    # TODO Doc
    r = {
        "code": str(code),
        "type": str(mtype),
        "message": str(msg)}
    return r


def random_string(string_length=20):
    """Generate a random string of fixed length """
    letters = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(letters) for i in range(string_length))


def fix_str(string):
    string = re.sub('[\'(),]', '', string)
    return string

def send_mail(mail,name,subject,textPart,htmlPart): # pragma: no cover

    api_key = "288ca9ac426b3e41809ee9c8a429a974"
    api_secret = "1f29a950828de1e093e7c8d4b74bd5ab"
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
                    {
                            "From": {
                                    "Email": "info@kelpa-api.herokuapp.com",
                                    "Name": "Kalepa Info"
                            },
                            "To": [
                                    {
                                            "Email": mail,
                                            "Name": name
                                    }
                            ],
                            "Subject": subject,
                            "TextPart": textPart,
                            "HTMLPart": htmlPart
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    return result.json()

