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

# Create your views here.


class StaffList(APIView, CustomPagination):
    
    
    paginator = PageNumberPagination()
    
    def get(self, request):
        obj = get_filter_query(Staff,request)
        page = self.paginate_queryset(obj,request)
        seri = StaffSerializer(page,many=True)
        
        return self.get_paginated_response(seri.data, status=status.HTTP_200_OK)

    def post(self, request):
        seri = StaffSerializer(data=request.data)
        
        if seri.is_valid():
            
            seri.validated_data["password"] = make_password(seri.validated_data["password"])
            seri.save()

            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffDetails(APIView):

    def get(self, request, obj_id):
        obj = get_object_or_404(Staff,pk=obj_id)
        seri = StaffSerializer(obj)

        return Response(seri.data, status=status.HTTP_200_OK)

    def put(self, request, obj_id):
        obj = get_object_or_404(Staff, pk=obj_id)
        seri = StaffSerializer(obj, data=request.data, partial=True)

        if seri.is_valid():
            seri.save()

            return Response(seri.data, status=status.HTTP_200_OK)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)



class DepartmentList(APIView):
    
    def get(self, request):
        obj = Department.objects.all()
        seri = DepartmentSerializer(obj,many=True)

        return Response(seri.data, status=status.HTTP_200_OK)

    def post(self, request):
        seri = DepartmentSerializer(data=request.data)

        if seri.is_valid():
            seri.save()

            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetails(APIView):

    def get(self, request, obj_id):
        obj = get_object_or_404(Department,pk=obj_id)
        seri = DepartmentSerializer(obj)

        return Response(seri.data, status=status.HTTP_200_OK)

    def put(self, request, obj_id):
        obj = get_object_or_404(Department, pk=obj_id)
        seri = DepartmentSerializer(obj, data=request.data, partial=True)

        if seri.is_valid():
            seri.save()

            return Response(seri.data, status=status.HTTP_200_OK)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)