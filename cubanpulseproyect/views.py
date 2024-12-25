from genericpath import samefile
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.staticfiles.utils import get_files
# Create your views here.

def index(request):
    return render(request, 'index.html')

#Services

#Paquetes de Viajes
def natural(request):
    return render(request, 'natural.html')

def hotels(request):
    return render(request, 'hotels.html')

def urban(request):
    return render(request, 'urban.html')

#Vista de login en el sistema de administacion
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Verificamos si el usuario es staff
                login(request, user)  # Iniciar sesión para el usuario staff
                return redirect('adminis')  # Redirige a la vista del admin (ajusta según tu configuración)
            else:
                login(request, user)  # Iniciar sesión para otros usuarios
                return redirect('index')  # Cambia esto por la vista deseada
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def create_account(request):
    return render(request,'create_account.html')

#Servicios
@login_required
def admin(request):
    return render(request,'admin.html')

#Administracion de la pagina
@login_required
def hotels_admin(request):
    return render(request,'hotels_admin.html')

@login_required
def natural_admin(request):
    return render(request,'natural_admin.html')

@login_required
def urban_admin(request):
    return render(request,'urban_admin.html')

#Administrar usuarios
@login_required
def administrar_usuarios(request):
    context={
        'usuarios': User.objects.all(),
    }
    return render(request,'administrar_usuarios.html',context)

#Deslogearse de la pagina
def salir(request):
    logout(request)
    return redirect('/')