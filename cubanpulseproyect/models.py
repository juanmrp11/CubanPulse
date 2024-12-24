from django.db import models

# Create your models here.

class Paquete(models.Model):
    titulo=models.CharField(max_length=50)
    precio=models.FloatField()
    descripcion=models.TextField()
    imagen=models.ImageField(upload_to='media/')
    fecha_creacion=models.DateField(auto_now_add=True)
    reservada=models.BooleanField(default=False)

    def __str__(self):
        return self.titulo