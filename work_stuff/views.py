from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.http import Http404
from staff_stuff.helpers import delete_helper, getlist_helper, getdetails_helper, post_helper, put_helper
from staff_stuff.pagination import CustomPagination
from .models import Work, StaffWork, Session, StaffSession
from .serializers import SessionSerializer, StaffSessionOnlySerializer, StaffSessionSerializer, WorkSerializer, StaffWorkSerializer, StaffWorkOnlySerializer

# Create your views here.
class WorkList(APIView,CustomPagination):
    def get(self, request):
        return getlist_helper(Work,request,WorkSerializer,self)

    def post(self, request):
        return post_helper(Work,request,WorkSerializer)


class WorkDetails(APIView):
    def get(self, request, obj_id):
        return getdetails_helper(Work,request, WorkSerializer,obj_id)

    def put(self, request, obj_id):
        return put_helper(Work, request, WorkSerializer, obj_id)

    def delete_helper(self, request, obj_id):
        return delete_helper(Work, request, WorkSerializer, obj_id)



class SessionList(APIView,CustomPagination):
    def get(self, request):
        return getlist_helper(Session,request,SessionSerializer,self)

    def post(self, request):
        return post_helper(Session,request,SessionSerializer)

class SessionDetails(APIView):
    def get(self, request, obj_id):
        return getdetails_helper(Session,request, SessionSerializer,obj_id)

    def put(self, request, obj_id):
        return put_helper(Session, request, SessionSerializer, obj_id)

    def delete_helper(self, request, obj_id):
        return delete_helper(Session, request, SessionSerializer, obj_id)


class StaffSessionList(APIView,CustomPagination):
    def get(self, request):
        return getlist_helper(StaffSession, request, StaffSessionSerializer,self)

    def post(self, request):
        return post_helper(StaffSession, request, StaffSessionOnlySerializer)

class StaffSessionDetails(APIView):
    def get(self, request, obj_id):
        return getdetails_helper(StaffSession,request,StaffSessionSerializer,obj_id)

    def delete(self, request, obj_id):
        return delete_helper(StaffSession,request,StaffSessionSerializer,obj_id)


class StaffWorkList(APIView,CustomPagination):
    def get(self, request):
        return getlist_helper(StaffWork,request,StaffWorkSerializer,self)

    def post(self, request):
        return post_helper(StaffWork,request,StaffWorkOnlySerializer)


class StaffWorkDetails(APIView):
    def get(self, request, obj_id):
        return getdetails_helper(StaffWork,request, StaffWorkSerializer,obj_id)

    def delete_helper(self, request, obj_id):
        return delete_helper(StaffWork, request, StaffWorkSerializer, obj_id)




