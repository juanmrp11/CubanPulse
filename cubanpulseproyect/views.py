from genericpath import samefile
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Paquete
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.staticfiles.utils import get_files
# Create your views here.

#---------------------------------------------------------------------------------------------------------------------------
def index(request):
    return render(request, 'index.html')

#---------------------------------------------------------------------------------------------------------------------------
#Services
#Paquetes de Viajes
def natural(request):
    context={
        'paquetes': Paquete.objects.all(),
    }
    return render(request, 'natural.html',context)

def hotels(request):
    return render(request, 'hotels.html')

def urban(request):
    context={
        'paquetes': Paquete.objects.all(),
    }
    return render(request, 'urban.html',context)

def details(request,id):
    context={
        'detalles': Paquete.objects.get(id=id),
    }
    return render(request, 'details.html',context)
#---------------------------------------------------------------------------------------------------------------------------
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
    if request.POST.get('nombre') and request.POST.get('apellidos') and request.POST.get('usuario') and request.POST.get('pass') and request.POST.get('correo'):
        usuario=User()
        usuario.first_name=request.POST.get('nombre')
        usuario.set_password(request.POST.get('pass'))
        usuario.username=request.POST.get('usuario')
        usuario.last_name=request.POST.get('apellidos')
        usuario.email=request.POST.get('correo')
        usuario.is_active=True
        
        usuario.save()
        return redirect(reverse('index'))
    else:
        return render(request,'create_account.html')

#Deslogearse de la pagina
def salir(request):
    logout(request)
    return redirect('/')



#---------------------------------------------------------------------------------------------------------------------------
#Administracion de la pagina
#Administrar Paquetes
@login_required
def paquetes_admin(request):
    if request.POST.get('titulo') and request.POST.get('precio') and request.POST.get('descripcion') and request.FILES.get('imagen') and request.POST.get('tipo'):
        paquete=Paquete()
        paquete.titulo=request.POST.get('titulo')
        paquete.precio=request.POST.get('precio')
        paquete.imagen=request.FILES.get('imagen')
        paquete.descripcion=request.POST.get('descripcion')
        paquete.tipo=request.POST.get('tipo')
        paquete.save()
        return redirect(reverse('adminis'))
    else:
        return render(request,'paquetes_admin.html')

#Index Admin
@login_required
def admin(request):
    context={
        'paquetes': Paquete.objects.all(),
    }
    return render(request,'admin.html',context)

#Administrar usuarios
@login_required
def administrar_usuarios(request):
    context={
        'usuarios': User.objects.all(),
    }
    return render(request,'administrar_usuarios.html',context)

#Eliminar paquete
@login_required
def eliminar_paquete(request,id):
    paquete=Paquete.objects.get(id=id)
    paquete.delete()
    return redirect(reverse('adminis'))

#Modificar paquete
@login_required
def modificar_paquete(request,id):
    paquete=Paquete.objects.get(id=id)
    
    if paquete.reservada==False:
        paquete.reservada=True
        paquete.save()
        return redirect(reverse('adminis'))
    else:
        paquete.reservada=False
        paquete.save()
        return redirect(reverse('adminis'))