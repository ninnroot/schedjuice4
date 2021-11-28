from schedjuice4.celery import app
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from celery.schedules import crontab

logger = get_task_logger(__name__)




    
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


    