from django.db import models

# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()
    img = models.CharField(max_length=50)
    totalProducto = models.CharField(max_length=50)