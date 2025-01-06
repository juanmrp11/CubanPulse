from genericpath import samefile
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Paquete, Servicio, Alojamiento, Imagen
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
    
    return render(request, 'natural.html')

def playa(request):
    return render(request, 'playa.html')

def urban(request):
    
    return render(request, 'urban.html')

def details(request,id):
    
    return render(request, 'details.html')


#---------------------------------------------------------------------------------------------------------------------------
#Login en el sistema
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
#Registarse en la web
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

#Index Admin
@login_required
def admin(request):
    
    return render(request,'admin.html')

#Administrar usuarios
@login_required
def administrar_usuarios(request):
    context={
        'usuarios': User.objects.all(),
    }
    return render(request,'administrar_usuarios.html',context)

#Administrar Paquetes
@login_required
def paquetes_admin(request):
    context={
        'hospedajes': Alojamiento.objects.all(),
    }
    return render(request,'paquetes_admin.html',context)
#Eliminar paquete
@login_required
def eliminar_paquete(request,id):
    paquete=Paquete.objects.get(id=id)
    paquete.delete()
    return redirect(reverse('adminis'))

#Administrar Alojamientos
@login_required
def alojamiento_admin(request):
    context={
        'alojamientos': Alojamiento.objects.all(),
    }
    if request.method == 'POST':
        # Guardar el alojamiento
        alojamiento = Alojamiento(
            nombre=request.POST.get('nombre'),
            ubicacion=request.POST.get('ubicacion'),
            precio=request.POST.get('precio'),
            descripcion=request.POST.get('descripcion'),
            tipo=request.POST.get('tipo'),
            cant_habitaciones=request.POST.get('habitaciones')
        )
        alojamiento.save()

        # Guardar las imágenes
        imagen_files = request.FILES.getlist('imagenes')  # Obtener la lista de archivos subidos
        for imagen_file in imagen_files:
            imagen = Imagen(imagen=imagen_file)
            imagen.save()
            alojamiento.imagen.add(imagen)  # Asociar la imagen al alojamiento

        return redirect('alojamiento_admin')
    return render(request, 'alojamiento_admin.html',context) 

#Eliminar Alojamiento
@login_required
def eliminar_alojamiento(request,id):
    alojamiento=Alojamiento.objects.get(id=id)
    alojamiento.delete()
    return redirect(reverse('adminis'))

#Administrar Servicios
@login_required
def servicios_admin(request):
    context={
        'servicios': Servicio.objects.all(),
    }
    if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('precio') and request.POST.get('noches'):
        servicio=Servicio()
        servicio.nombre=request.POST.get('nombre')
        servicio.descripcion=request.POST.get('descripcion')
        noches = request.POST.get('noches')
        servicio.cant_dias = int(noches) if noches else None
        print(f"cant_dias: {servicio.cant_dias}") 
        servicio.precio=request.POST.get('precio')
        try:
            servicio.save()
        except Exception as e:
            print(f"Error al guardar el servicio: {e}")
        return redirect(reverse('servicios_admin'))
    else:
        return render(request,'servicios_admin.html',context)
    
#Eliminar
@login_required
def eliminar_servicio(request,id):
    servicio=Servicio.objects.get(id=id)
    servicio.delete()
    return redirect(reverse('servicios_admin'))

#Administrar Imagenes
@login_required
def imagenes_admin(request):
    context={
        'imagenes': Imagen.objects.all(),
    }
    if request.POST.get('tipoi') and request.FILES.get('imagen'):
        imagen=Imagen()
        imagen.tipo=request.POST.get('tipoi')
        imagen.imagen=request.FILES.get('imagen')
        imagen.save()
        return redirect(reverse('imagenes_admin'))
    else:
        return render(request,'imagenes_admin.html',context)

#Eliminar Imagen
@login_required
def eliminar_imagen(request,id):
    imagen=Imagen.objects.get(id=id)
    imagen.delete()
    return redirect(reverse('imagenes_admin'))
