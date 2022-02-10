from schedjuice4.celery import app
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from celery.schedules import crontab
import requests

from work_stuff.models import Work
from datetime import date


logger = get_task_logger(__name__)

# IMPORTANT !
# after modifying tasks, don't forget to restart the celery services on the server.

app.conf.beat_schedule={
    
    "repopulate": {
        "task": "repopulate",
        "schedule": crontab(minute=0, hour=0),
    },
    "work_activator":{
        "task": "work_activator",
        "schedule": crontab(minute=0,hour=0)
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


@app.task(name="work_activator")
def work_activator():
    works = Work.objects.filter(status="ready").all()
    for i in works:

        if (i.valid_from - date.today()).days == 1:
            pass
        
        elif (i.valid_from <= date.today()):
            i.status="active"
            i.save()

        elif (i.valid_to - date.today()).days == 1:
            pass

        elif i.valid_to <= date.today():
            i.status = "ended"
            i.save()


    