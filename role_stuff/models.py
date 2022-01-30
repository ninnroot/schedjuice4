from django.db import models
from rest_framework.serializers import ValidationError

# Create your models here.

class Role(models.Model):
    
    name = models.CharField(max_length=256, unique=True)
    shorthand = models.CharField(max_length=6,unique=True)
    description = models.TextField(default="...")
    is_specific = models.BooleanField()
    deletable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":[
            "shorthand",
            "created_at",
            "updated_at",
        ],
    }

    def delete(self,*args,**kwargs):
        if self.deletable:
            raise ValidationError("This is a system role and cannot be deleted.")

        return super().delete(*args,**kwargs)

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
        ordering = ["name"]