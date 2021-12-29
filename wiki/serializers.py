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
        print(i)
        if p is None:

            bigger = Topic.objects.filter(parent__isnull=True,index__gte=i).all()
        else:
            bigger = Topic.objects.filter(parent=p,index__gte=i).all()

        for i in bigger:
            i.index +=1
            i.save()
        
        
        topic = super().create(data)
        topic.save()

        return topic

    



    class Meta:
        model = Topic
        fields = "__all__"


class TopicSerializerWithChildren(DynamicFieldsModelSerializer):
    
    children = TopicSerializer(source="parent_set", many=True, read_only=True)
    tags = TagOnlySerializer(source="tag_set", many=True, read_only=True)

    def update(self, instance, data):
        p=instance.parent
        i=data.get("index")
        if p is None:
            smaller = Topic.objects.filter(parent__isnull=True,index__lt=i, index__gt=instance.index).all()

        else:
            smaller = Topic.objects.filter(parent=p,index__lt=i, index__gt=instance.index).all()

        for i in smaller:
            i.objects.update(index=i.index-1)
            i.save()
        instance.index = i
        instance.save()

        return instance

    class Meta:
        model = Topic
        fields = "__all__"