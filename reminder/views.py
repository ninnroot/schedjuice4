from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.http import Http404
from django.core.mail import send_mail
import json

# Create your views here.

class SendMail(APIView):

    def post(self, request, format=None):
        data = request.data
        subj = data["subject"]
        body = data["body"]
        recepients = json.loads(data["recepients"])
        
        send_mail(
                  subj,
                  body,
                  "robotjames.beepboop@gmail.com",
                  recepients,
                  auth_user="robotjames.beepboop@gmail.com",
                  auth_password="weemannogoodXD"

                   )
        
        
        return Response({"message":"ok"}, status=status.HTTP_200_OK)

