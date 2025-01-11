from django.db import models

# Create your models here.
class Imagen(models.Model):
    imagen=models.ImageField(upload_to='media/')
    tipo=models.CharField(max_length=20)

#Servicios
#Servicios playa
class Servicio(models.Model):
    nombre=models.CharField(max_length=20)
    descripcion=models.TextField(max_length=1000)
    precio=models.FloatField()
    tipo=models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

#Alojamiento
class Alojamiento(models.Model):
    nombre=models.CharField(max_length=20)
    ubicacion=models.CharField(max_length=200)
    descripcion=models.TextField(max_length=1500)
    precio=models.FloatField(null=True,blank=True)
    lleno=models.BooleanField(default=False)
    tipo=models.CharField(max_length=50)
    imagen=models.ManyToManyField(Imagen,related_name='alojamiento')
    def __str__(self):
        return self.nombre

#Paquetes
class Paquete(models.Model):
    nombre=models.CharField(primary_key=True,max_length=20)
    tipo=models.CharField(max_length=20)
    duracion_dias=models.IntegerField()
    duracion_noches=models.IntegerField()
    descripcion=models.TextField(max_length=5000)
    hospedaje=models.ManyToManyField(Alojamiento,related_name='paquete')
    servicios=models.ManyToManyField(Servicio,related_name='paquete')
    imagen=models.ImageField(upload_to='media/')

    def __str__(self):
        return self.nombre
    
    

