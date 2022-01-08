from schedjuice4.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from .models import Role

class RoleOnlySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"

class RoleSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"