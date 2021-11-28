from time import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.http import Http404
from django.core.mail import send_mail
from .tasks import send_mail_task
from decouple import config
from celery.result import AsyncResult
from time import perf_counter
import json
# Create your views here.

class SendMail(APIView):

    def post(self, request, format=None):
        data = request.data
        subj = data["subject"]
        body = data["body"]
        recepients = json.loads(data["recepients"])
        a = perf_counter()
        
        x = send_mail_task.delay(
                  subj,
                  body,
                  "noreply@teachersucenter.com",
                  recepients,
                  
                   )
        
    
        return Response({"message":f"time: {perf_counter() - a}"}, status=status.HTTP_200_OK)

