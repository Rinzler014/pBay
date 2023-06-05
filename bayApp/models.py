from django.db import models

# Create your models here.

class producto(models.Model):
    nameModel = models.CharField(max_length=50)
    descriptionModel = models.CharField(max_length=100)
    priceModel = models.IntegerField()
    imgModel = models.CharField(max_length=200)
    totalProductModel = models.CharField(max_length=50)