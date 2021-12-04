from django.db.models import fields
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers, status
from django.db import models
from rest_framework.request import Request
from .filter import get_filter_query


def fields_helper(request:Request):
    fields = None
    if "fields" in request.query_params:
        fields=request.query_params.get("fields")
    return fields

def getlist_helper(model:models.Model, request:Request, serializer:ModelSerializer, obj):
    query = get_filter_query(model,request)
    page = obj.paginate_queryset(query,request)
    fields=fields_helper(request)
    if fields:
        seri = serializer(page,many=True,fields=fields)
    else:
        seri = serializer(page,many=True)

    return obj.get_paginated_response(seri.data, status=status.HTTP_200_OK)

def getdetails_helper(model:models.Model, request:Request,serializer:ModelSerializer,pk):
    obj = get_object_or_404(model,pk=pk)
    fields=fields_helper(request)
    if fields:
        seri = serializer(obj,fields=fields)
    else:
        seri = serializer(obj)
    return Response(seri.data, status=status.HTTP_200_OK)

def post_helper(model:models.Model, request:Request, serializer:Serializer):
        seri = serializer(data=request.data)
        if seri.is_valid():
            seri.save()
            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

def put_helper(model:models.Model, request:Request, serializer:Serializer, pk):
    obj = get_object_or_404(model,pk=pk)
    seri = serializer(obj,data=request.data,partial=True)
    
    if seri.is_valid():
        seri.save()

        return Response(seri.data, status=status.HTTP_200_OK)
    return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_helper(model:models.Model, request:Request, serializer:Serializer, pk):
    obj = get_object_or_404(model,pk=pk)
    seri = serializer(obj).data
    obj.delete()

    return Response(seri, status=status.HTTP_200_OK)


