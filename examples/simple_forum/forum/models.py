from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Thread(models.Model):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, related_name='threads')



