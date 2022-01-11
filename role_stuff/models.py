from django.db import models

# Create your models here.

class Role(models.Model):

    name = models.CharField(max_length=256, unique=True)
    shorthand = models.CharField(max_length=6,unique=True)
    description = models.TextField(default="...")
    is_specific = models.BooleanField()
    
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
    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
        ordering = ["name"]