from rest_framework import serializers

from .models import Topic, TopicTag
from work_stuff.serializers import DynamicFieldsModelSerializer

class TagOnlySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = TopicTag
        fields = "__all__"

class TopicOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Topic
        fields = ["title", "parent", "index"]


class TagSerializer(DynamicFieldsModelSerializer):
    topics = TopicOnlySerializer(source="topic_set", many=True, read_only=True)

    class Meta:
        model = TopicTag
        fields = "__all__"

class TopicSerializer(DynamicFieldsModelSerializer):
    
    tags = TagOnlySerializer(source="tag_set", many=True, read_only=True)


    def create(self, data):
        p = data.get("parent")
        i = data.get("index")
        bigger = Topic.objects.filter(parent=p,index__gt=i).all()

        for i in bigger:
            i.index +=1
        Topic.objects.bulk_update(bigger,["index"])
        
        topic = super().create(data)
        topic.save()

        return topic

    def update(self, instance, data):
        p=instance.parent
        i=data.get("index")
        smaller = Topic.objects.filter(parent=p,index__lt=i, index__gt=instance.index).all()

        for i in smaller:
            i.index -=1
        Topic.objects.bulk_update(smaller,["index"])
        instance.index = i
        instance.save()

        return instance



    class Meta:
        model = Topic
        fields = "__all__"


class TopicSerializerWithChildren(DynamicFieldsModelSerializer):
    
    children = TopicSerializer(source="parent_set", many=True, read_only=True)
    tags = TagOnlySerializer(source="tag_set", many=True, read_only=True)
    

    class Meta:
        model = Topic
        fields = "__all__"