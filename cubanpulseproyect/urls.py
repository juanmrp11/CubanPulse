from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    #Url principal
    path('',views.index,name="index"),
    
    #Url de login de los usuarios de administracion de la pagina
    path('accounts/login/', views.login_view, name='login'),
    path('administracion/', views.admin,name="adminis"),
    
    #Url de administracion
    #Paquetes
    path('administracion/paquetes', views.paquetes_admin,name='paquetes_admin'),
    path('administracion/eliminar_paquete/<id>', views.eliminar_paquete,name='eliminar_paquete'),
    #Usuarios
    path('administracion/usuarios',views.administrar_usuarios,name='usuarios'),
    #Alojamiento
    path('administracion/alojamiento',views.alojamiento_admin,name='alojamiento_admin'),
    path('administracion/eliminar_alojamiento/<id>', views.eliminar_alojamiento,name='eliminar_alojamiento'),
    #Servicios
    path('administracion/servicios',views.servicios_admin,name='servicios_admin'),
    path('administracion/eliminar_servicio/<id>',views.eliminar_servicio,name='eliminar_servicio'),
    #Imagenes
    path('administracion/imagenes',views.imagenes_admin,name='imagenes_admin'),
    path('administracion/eliminar_imagen/<id>', views.eliminar_imagen,name='eliminar_imagen'),
    
    #Url de deslogearse
    path('salir/',views.salir,name='salir'),
    
    #Url de registrarse en la pagina
    path('create_account', views.create_account,name='create_account'),
    
    #Url Servicios
    #Paquetes de Viaje
    path('natural/',views.natural,name="natural"),
    path('playa/',views.playa,name="playa"),
    path('urban/',views.urban,name="urban"),
    path('natural/details/<id>',views.details,name='details'),
    path('urban/details/<id>',views.details,name='details'),
    
]