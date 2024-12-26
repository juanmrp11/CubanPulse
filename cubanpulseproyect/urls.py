from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    #Url principal
    path('',views.index,name="index"),
    
    #Url de login de los usuarios de administracion de la pagina
    path('accounts/login/', views.login_view, name='login'),
    path('administracion/', views.admin,name="adminis"),
    path('administracion/paquetes', views.paquetes_admin,name='paquetes_admin'),
    path('administracion/eliminar/<id>', views.eliminar_paquete,name='eliminar_paquete'),
    path('administracion/reservada/<id>', views.modificar_paquete,name='modificar_paquete'),
    path('administracion/usuarios',views.administrar_usuarios,name='usuarios'),
    
    #Url de deslogearse
    path('salir/',views.salir,name='salir'),
    
    #Url de registrarse en la pagina
    path('create_account', views.create_account,name='create_account'),
    
    #Url Servicios
    #Paquetes de Viaje
    path('natural/',views.natural,name="natural"),
    path('hotels/',views.hotels,name="hotels"),
    path('urban/',views.urban,name="urban"),
    path('natural/details/<id>',views.details,name='details'),
    path('urban/details/<id>',views.details,name='details'),
    
]