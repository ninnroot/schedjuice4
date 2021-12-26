from django.db.models.fields import related
from django.shortcuts import render
from rest_framework import serializers
from staff_stuff.views import GeneralList,GeneralDetails
from .serializers import TopicSerializer, TopicSerializerWithChildren, TagSerializer
from .models import Topic, TopicTag

class TopicList(GeneralList):
    model = Topic
    serializer = TopicSerializer
    

class TopicDetails(GeneralDetails):
    model = Topic
    serializer = TopicSerializerWithChildren



class TopicTagList(GeneralList):
    model = TopicTag
    serializer = TagSerializer
    related_fields = ["topic_set"]
    

class TopicTagDetails(GeneralDetails):
    model = TopicTag
    serializer = TagSerializer
    related_fields = ["topic_set"]
