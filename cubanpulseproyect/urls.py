from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    #Url principal
    path('',views.index,name="index"),
    
    #Url de login de los usuarios de administracion de la pagina
    path('accounts/login/', views.login_view, name='login'),
    path('administracion', views.admin,name="adminis"),
    path('administracion/hotels_admin', views.hotels_admin,name='hotels_admin'),
    path('administracion/natural_admin', views.natural_admin,name='natural_admin'),
    path('administracion/urban_admin', views.urban_admin,name='urban_admin'),
    path('administracion/usuarios',views.administrar_usuarios,name='usuarios'),
    
    #Url de deslogearse
    path('salir/',views.salir,name='salir'),
    
    #Url de registrarse en la pagina
    
    #Url Servicios
    #Paquetes de Viaje
    path('natural',views.natural,name="natural"),
    path('hotels',views.hotels,name="hotels"),
    path('urban',views.urban,name="urban"),
    
]