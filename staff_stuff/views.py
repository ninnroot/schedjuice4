from functools import partial
from django.core import paginator
from django.db.models import manager
from django.shortcuts import render
from rest_framework import pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import serializers, status
from django.http import Http404
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings
from .pagination import CustomPagination


from .models import Department, Staff
from .serializers import DepartmentSerializer, StaffSerializer
from .filter import get_filter_query
from .helpers import delete_helper, getlist_helper, getdetails_helper, post_helper, put_helper

# Create your views here.


class StaffList(APIView, CustomPagination):
    
    
    def get(self, request):
        return getlist_helper(Staff,request,StaffSerializer,self)

    def post(self, request):
        seri = StaffSerializer(data=request.data)
        
        if seri.is_valid():
            
            seri.validated_data["password"] = make_password(seri.validated_data["password"])
            seri.save()

            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffDetails(APIView):

    def get(self, request, obj_id):
        return getdetails_helper(Staff,request,StaffSerializer,obj_id)

    def put(self, request, obj_id):
        obj = get_object_or_404(Staff, pk=obj_id)
        seri = StaffSerializer(obj, data=request.data, partial=True)

        if seri.is_valid():
            seri.save()

            return Response(seri.data, status=status.HTTP_200_OK)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,obj_id):
        return delete_helper(Staff,request,StaffSerializer,obj_id)


class DepartmentList(APIView,CustomPagination):
    
    def get(self, request):
        return getlist_helper(Department,request,DepartmentSerializer,self)

    def post(self, request):
        return post_helper(Department,request,DepartmentSerializer)

class DepartmentDetails(APIView):

    def get(self, request, obj_id):
        return getdetails_helper(Department,request,DepartmentSerializer,obj_id)

    def put(self, request, obj_id):
        return put_helper(Department,request,DepartmentSerializer,obj_id)

    def delete(self, request,obj_id):
        return delete_helper(Department,request,DepartmentSerializer,obj_id)

