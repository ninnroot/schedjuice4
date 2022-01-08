from rest_framework.generics import get_object_or_404
from schedjuice4.generic_views import GeneralList,GeneralDetails
from .serializers import TopicSerializer, TopicSerializerWithChildren, TagSerializer
from .models import Topic, TopicTag


class TopicList(GeneralList):
    model = Topic
    serializer = TopicSerializer
    

class TopicDetails(GeneralDetails):
    model = Topic
    serializer = TopicSerializerWithChildren

    def delete(self, request, obj_id):
        obj = get_object_or_404(self.model, pk=obj_id)
        bigger = Topic.objects.filter(parent=obj.parent,index__gt=obj.index).all()
        for i in bigger:
            i.index -= 1
            i.save()
        return super().delete(request, obj_id)



class TopicTagList(GeneralList):
    model = TopicTag
    serializer = TagSerializer
    related_fields = ["topic_set"]
    

class TopicTagDetails(GeneralDetails):
    model = TopicTag
    serializer = TagSerializer
    related_fields = ["topic_set"]
