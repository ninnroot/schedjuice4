import csv

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from rest_framework.request import Request
from .filter import get_filter_query

from ms_stuff.exceptions import MSException
from rest_framework.serializers import ValidationError

from staff_stuff.models import Staff


def get_excluded(self,request):
    excluded_fields = []
    if hasattr(self.model, "excluded_fields"):
        excluded_fields = self.model.excluded_fields[get_role(request)]

    return excluded_fields

def get_role(request):
    return Staff.objects.get(pk=request.user.id).role.shorthand

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
        read_only_fields=self.model.read_only_fields[get_role(request)],
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
        read_only_fields=self.model.read_only_fields[get_role(request)],
        excluded_fields=get_excluded(self,request),
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
            read_only_fields=self.model.read_only_fields[get_role(request)],
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
        data=request.data,partial=True,
        read_only_fields=self.model.read_only_fields[get_role(request)],
        excluded_fields=get_excluded(self,request),
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

    


