
import random
import csv

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from rest_framework.request import Request
from .filter import get_filter_query, get_fields_from_request

from ms_stuff.exceptions import MSException
from rest_framework.serializers import ValidationError

from staff_stuff.models import Staff

from datetime import date

def get_read_only(self,request,obj_id=None):
    rd = []
    x=get_user(request)
    if obj_id:
        if obj_id == x.id and self.model.__name__ == "Staff":
            return rd
    return self.model.read_only_fields[x.role.shorthand]

def get_excluded(self,request, obj_id=None):
    excluded_fields = []
    x = get_user(request)
    if obj_id:
        if obj_id == x.id and (self.model.__name__ == "Staff"):
            return excluded_fields
    if hasattr(self.model, "excluded_fields"):
        excluded_fields = self.model.excluded_fields[x.role.shorthand]

    return excluded_fields

def get_user(request):
    return Staff.objects.get(pk=request.user.id)

def get_csv(self,seri):
    res = HttpResponse(content_type="text/csv")
    res['Content-Disposition'] = f'attachment; filename="export.csv"'
    
    non_relations = [i.name for i in self.model._meta.fields if not i.is_relation]

    writer = csv.writer(res)
    lst = []
    for i in seri.data[0]:
        if i in non_relations:
            lst.append(i)
    writer.writerow(lst)

    for i in seri.data:
        lst = []    
        for j in i:
            if j in non_relations:
                lst.append(i[j])
        writer.writerow(lst)
    
    return res



def getlist_helper(self,request:Request):
    
    if request.GET.get("utility"):
        
        return Response({"fields":sorted([i.name for i in self.model._meta.get_fields()])})
    
    

    if not hasattr(self,"related_fields"):
        self.related_fields = []
        
    query = get_filter_query(self.model,request,pre=self.related_fields)
    page = self.paginate_queryset(query,request)
    
    

    seri = self.serializer(
        page,many=True,
        fields=request.query_params.get("fields"),
        read_only_fields=get_read_only(self,request),
        excluded_fields=get_excluded(self,request),
        context={"r":request}
        )
    
    if request.GET.get("csv"):
        return get_csv(self,seri)
        
    return self.get_paginated_response(seri.data, status=status.HTTP_200_OK)


def getdetails_helper(self,request:Request,obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    self.check_object_permissions(self.request,obj)
    
    seri = self.serializer(
        obj,
        fields=request.query_params.get("fields"),
        read_only_fields=get_read_only(self, request, obj_id),
        excluded_fields=get_excluded(self,request,obj_id),
        context={"r":request}
        )

    if request.GET.get("csv"):
        return get_csv(self,seri)
    
    return Response(seri.data, status=status.HTTP_200_OK)


def post_helper(self, request:Request):
        silent = request.query_params.get("silent")
        if silent is None:
            silent = False
            
        seri = self.serializer(
            data=request.data,
            read_only_fields=get_read_only(self, request),
            excluded_fields=get_excluded(self,request),
            context={"r":request,"silent":silent}
        )
        if seri.is_valid():

            seri.save()
            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)


def put_helper(self,request:Request, obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    
    self.check_object_permissions(self.request,obj)
    
    seri = self.serializer(
        obj,
        data=request.data,
        partial=True,
        read_only_fields=get_read_only(self, request, obj_id),
        excluded_fields=get_excluded(self,request,obj_id),
        context={"r":request}
        )
    
    if seri.is_valid():
        seri.save()


        return Response(seri.data, status=status.HTTP_200_OK)
    return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_helper(self,request:Request, obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    seri = self.serializer(obj,context={"r":request}).data

    try:
        silent = request.query_params.get("silent")
        if silent is None:
            silent = False
 
        obj.delete(r=request,silent=silent)
     
        return Response(seri, status=status.HTTP_200_OK)
    

    except MSException or ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


def is_requirement_satisfied(self, request):
    for i in get_fields_from_request(self.model, request):
        if i in self.GET:
            continue
        return True
    return False


def search_helper(self,request:Request):

    fields = get_fields_from_request(self.model, request)
    all_fields = request.GET.get("all")

    if len(fields) == 0 and not all_fields:
        return Response({"error":"The request must contain either 'all' param or at least one of the resource's fields"}, status=status.HTTP_400_BAD_REQUEST)

    if not hasattr(self,"related_fields"):
        self.related_fields = []
    
    legit_fields = [i.name for i in self.model._meta.get_fields() if i.get_internal_type() in ["CharField", "EmailField"]]

    queryset = self.model.objects.all()

    if all_fields:
        q = QuerySet.union(*[
            queryset.annotate(similarity=TrigramSimilarity(str(i), str(all_fields))).filter(similarity__gt=0.35) 
            for i in legit_fields
            ])

    if not all_fields:
        q = QuerySet.union(*[
        queryset.annotate(similarity=TrigramSimilarity(i, fields[i])).filter(similarity__gt=0.35)
        for i in fields
    ])

    page = self.paginate_queryset(q,request)
    

    seri = self.serializer(
        page,many=True,
        fields=request.query_params.get("fields"),
        read_only_fields=get_read_only(self,request),
        excluded_fields=get_excluded(self,request),
        context={"r":request}
        )
    
    if request.GET.get("csv"):
        return get_csv(self,seri)
        
    return self.get_paginated_response(seri.data, status=status.HTTP_200_OK)



    




