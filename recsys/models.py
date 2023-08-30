from django.db import models


# Create your models here.
class News(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    Category = models.CharField(max_length=50)
    SubCategory = models.CharField(max_length=50)
    Title = models.CharField(max_length=100)
    Abstract = models.CharField(max_length=1000)
    URL = models.CharField(max_length=100)
    TitleEntities = models.CharField(max_length=1000)
    AbstractEntities = models.CharField(max_length=1000)

    class Meta:
        db_table = "News"


class Behaviors(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    field2 = models.CharField(max_length=50)
    field3 = models.CharField(max_length=50)
    field4 = models.CharField(max_length=1000)
    field5 = models.CharField(max_length=1000)

    class Meta:
        db_table = "Behaviors"