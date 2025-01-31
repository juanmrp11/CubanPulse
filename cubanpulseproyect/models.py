from django.db import models
from django.contrib.auth.models import User
import json
from datetime import datetime, timedelta

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

class FechaOcupada(models.Model):
    fecha = models.DateField()

    def __str__(self):
        return self.fecha.__str__()

def default_disponibilidad():
    # Devuelve una cadena JSON por defecto
    return json.dumps([{
        "desde": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "hasta": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    }])

#Alojamiento
class Alojamiento(models.Model):
    nombre=models.CharField(max_length=20)
    ubicacion=models.CharField(max_length=200)
    descripcion=models.TextField(max_length=1500)
    precio=models.FloatField(null=True,blank=True)
    tipo=models.CharField(max_length=50)
    imagen=models.ManyToManyField(Imagen,related_name='alojamiento')
    disponibilidad = models.TextField(blank=True, null=True)
    
    def get_disponibilidad(self):
        if self.disponibilidad:
            return json.loads(self.disponibilidad)
        return []
    
    def set_disponibilidad(self, value):
        # Guarda la disponibilidad como una cadena JSON
        self.disponibilidad = json.dumps(value) if value else json.dumps([])

#Paquetes
class Paquete(models.Model):
    nombre=models.CharField(primary_key=True,max_length=20)
    tipo=models.CharField(max_length=20)
    descripcion=models.TextField(max_length=5000)
    hospedaje=models.ManyToManyField(Alojamiento,related_name='paquete')
    servicios=models.ManyToManyField(Servicio,related_name='paquete')
    imagen=models.ImageField(upload_to='media/')

    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)  # Relación con el paquete
    servicios = models.ManyToManyField(Servicio, related_name='reservas')  # Servicios seleccionados
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.CASCADE)  # Alojamiento seleccionado
    fecha_inicio = models.DateField()  # Fecha de inicio
    fecha_fin = models.DateField()  # Fecha de fin
    precio_total = models.FloatField()  # Precio total

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.paquete.nombre}"
    

