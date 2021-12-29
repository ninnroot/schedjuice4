from django.db import models
from django.db.models.deletion import CASCADE

class TopicTag(models.Model):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    color = models.CharField(max_length=7,default="#000000")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'topic_tag'
        verbose_name_plural = 'topic_tags'
        ordering = ["id"]

class Topic(models.Model):

    title = models.JSONField()
    content = models.JSONField()
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    index = models.IntegerField()
    image = models.ImageField(null=True, upload_to="topic_pics")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"
        ordering = ["id"]

class TopicTagRelation(models.Model):

    topic = models.ForeignKey(Topic, on_delete=CASCADE)
    tag = models.ForeignKey(TopicTag,on_delete=CASCADE)

    class Meta:
        verbose_name = "topictag"
        verbose_name_plural = "topictags"

        ordering = ["id"]