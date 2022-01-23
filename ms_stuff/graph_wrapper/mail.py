import base64
import imp
from jinja2_stuff.core import env

from .base import MSRequest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from .config import constants

class MailMS(MSRequest):
    
    def __init__(self):
        super().__init__()
        MailMS.headers = {
            "Authorization": "Bearer "+self.token,
            "Content-Type": "text/plain"
        }

    def make_template(self, template: str, context):
        t = env.get_template(template)

        return t.render(context=context)

    def _send(self, sender, receiver, content):

        message = MIMEMultipart("alternative")
        message["Subject"] = content["subject"]
        message["From"] = sender
        message["To"] = receiver

        text = MIMEText(content["text"], "plain")
        

        message.attach(text)
        if "context" in content:
            html = MIMEText(self.make_template(
                content["template"], content["context"]), "html")
            message.attach(html)

        message = base64.encodebytes(message.as_bytes())

        return self.post(f"users/{sender}/sendMail", message, encode=False)


    def send_welcome(self, sender: str, receiver: str, context, subj="Welcome to Teacher Su center"):

        text = f"Welcome to Teacher Su centre.\n\n"\
            f"Greetings, {context['name']}. Let's get you started. Go to this link"\
            f"(https://youtu.be/dQw4w9WgXcQ) to start learning about MS Teams.\n"\
            f"The following are your credentials:\n"\
            f"Email: {context['email']}\n"\
            f"Password: {context['password']}\n\n\n"\
            f"This is a system generated message. Please do not reply to this. For IT enquiries, "\
            f"you may email us at techgeeks@teachersucenter.com."

        content = {
            "subject": subj,
            "context": context,
            "template": "welcome.html",
            "text": text
        }
        return self._send(sender, receiver, content=content)


    def send_from_request(self, request):
        text = request.data.get("text")
        
        if request.data.get("system"):
            text+="\n\nThis is a system generated email. Please do not reply to this.\n"\
                "For IT enquiries, you may email as at techgeeks@teachersucenter.com"

        content = {
            "subject":request.data.get("subject"),
            "text":text

        }
        return self._send(constants["STAFFY_ID"],request.data.get("receiver"),content=content)
