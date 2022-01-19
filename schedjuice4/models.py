from django.db import models


class CustomModel(models.Model):

    def delete(self, *args, **kwargs):
        try:
            for i in ["r", "silent"]:
                kwargs.pop(i)
        except KeyError:
            pass
        return super().delete(*args, **kwargs)

    class Meta:
        abstract = True