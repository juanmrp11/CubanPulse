from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  # For date manipulation

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
    reservado=models.BooleanField(default=False)
    tipo=models.CharField(max_length=50)
    imagen=models.ManyToManyField(Imagen,related_name='alojamiento')
    
    def esta_disponible(self, fecha_inicio, fecha_fin):
        # Convertir las fechas de entrada a objetos de fecha
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        # Verifica si hay reservas que se superpongan con las fechas solicitadas
        reservas = Reserva.objects.filter(
            alojamiento=self,
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio
        )
        return not reservas.exists()  # Devuelve True si no hay reservas que se superpongan

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

