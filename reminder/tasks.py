from schedjuice4.celery import app
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from celery.schedules import crontab
import requests
logger = get_task_logger(__name__)


app.conf.beat_schedule={
    
    "repopulate": {
        "task": "repopulate",
        "schedule": crontab(minute=0, hour=0),
    
    }
}

@app.task(name="repopulate")
def repopulate():
    requests.get("https://api.teachersucenter.com/api/formgen/repopulate")
    
@app.task(name="send_mail_task")
def send_mail_task(subject, body, mail_from, mail_to):
    x = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=mail_from,
                    to=mail_to,
                    )
    x.send()
    return True


    