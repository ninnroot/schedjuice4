from schedjuice4.celery import app
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@app.task(name="send_mail_task")
def send_mail_task(subject, body, mail_from, mail_to, auth_user,auth_password):
    x = send_mail(subject, body, mail_from, mail_to, auth_user=auth_user,auth_password=auth_password)
    print(x)
    return True
    