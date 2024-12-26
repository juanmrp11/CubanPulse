from django.db import models

# Create your models here.

#Paquetes
class Paquete(models.Model):
    titulo=models.CharField(max_length=50)
    tipo=models.CharField(max_length=50,null=True)
    precio=models.FloatField(null=True)
    descripcion=models.TextField()
    imagen=models.ImageField(upload_to='media/')

    def __str__(self):
        return self.titulo

#Alojamiento
class Alojamientos(models.Model):
    cantidad_habitaciones=models.IntegerField()
    ubicacion=models.CharField(max_length=100)
    precio=models.FloatField()
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

#Viajes
class Viajes(models.Model):
    destino=models.CharField(max_length=100)
    cantidad_personas=models.IntegerField()
    precio=models.FloatField()

    def __str__(self):
        return self.destino

#Otros Servicios
class Otros_Servicios():
    nombre=models.CharField(max_length=100)
    precio=models.FloatField()

    def __str__(self):
        return self.nombre

#Reservaciones
class Reservaciones(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='reservaciones')
    viajes = models.ForeignKey(Viajes, on_delete=models.CASCADE)
    alojamiento = models.ForeignKey(Alojamientos, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    fecha_entrada = models.DateField(max_length=100)
    fecha_salida = models.DateField(max_length=100)
    transporte = models.BooleanField(default=False)
    comidas = models.CharField(max_length=100)
    celulares = models.BooleanField(default=False)
    otros_servicios = models.TextField(blank=True)  # Para otros servicios que no estén en la lista

    def __str__(self):
        return f"Reservación de {self.nombre_cliente} para {self.paquete.nombre}"
    
