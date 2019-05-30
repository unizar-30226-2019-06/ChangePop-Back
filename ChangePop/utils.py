import random
import re
import string

from mailjet_rest import Client
import os

from ChangePop.models import Notifications


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


def push_notify(user_id, text, product=None, category=None):
    Notifications.push(user_id, text, product=product, category=category)


def fix_str(string):
    string = re.sub('[\'(),]', '', string)
    return string


def send_mail(mail,name,subject,textPart,htmlPart): # pragma: no cover

    api_key = os.environ.get('MAIL_API')
    api_secret = os.environ.get('MAIL_KEY')
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

