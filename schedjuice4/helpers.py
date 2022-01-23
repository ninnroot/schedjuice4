from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from rest_framework.request import Request
from .filter import get_filter_query

from ms_stuff.exceptions import MSException



def getlist_helper(self,request:Request):
    
    if request.query_params.get("utility") == "True":
        
        return Response({"fields":sorted([i.name for i in self.model._meta.get_fields()])})
    if not hasattr(self,"related_fields"):
        self.related_fields = []
    query = get_filter_query(self.model,request,pre=self.related_fields)
    page = self.paginate_queryset(query,request)
    
    seri = self.serializer(
        page,many=True,
        fields=request.query_params.get("fields"),
        read_only_fields=self.read_only_fields,
        excluded_fields=self.excluded_fields,
        context={"r":request}
        )
    
    
    return self.get_paginated_response(seri.data, status=status.HTTP_200_OK)


def getdetails_helper(self,request:Request,obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    self.check_object_permissions(self.request,obj)
    
    seri = self.serializer(
        obj,
        fields=request.query_params.get("fields"),
        read_only_fields=self.read_only_fields,
        excluded_fields=self.excluded_fields,
        context={"r":request}
        )
    
    return Response(seri.data, status=status.HTTP_200_OK)


def post_helper(self, request:Request):
        silent = request.query_params.get("silent")
        if silent is None:
            silent = False
            
        seri = self.serializer(
            data=request.data,
            read_only_fields=self.read_only_fields,
            excluded_fields=self.excluded_fields ,
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
        read_only_fields=self.read_only_fields,
        excluded_fields=self.excluded_fields,
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
    
    except MSException as e:
        return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    


