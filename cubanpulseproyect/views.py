from genericpath import samefile
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Paquete, Servicio, Alojamiento, Imagen, Reserva
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.staticfiles.utils import get_files
from django.core.mail import send_mail
from django.conf import settings

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

def playa(request):
    context={
        'paquetes': Paquete.objects.all(),
    }
    return render(request, 'playa.html',context)

def urban(request):
    context={
        'paquetes': Paquete.objects.all(),
    }
    return render(request, 'urban.html',context)

@login_required
def details(request, id):
    paquete = Paquete.objects.get(nombre=id)
    alojamientos_disponibles = []
    
    if request.method == 'POST':
        servicios_ids = request.POST.getlist('servicios')
        alojamiento_id = request.POST.get('alojamiento_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        precio_total = request.POST.get('precio_total')

        # Verificar si las fechas son válidas
        if not fecha_inicio or not fecha_fin:
            messages.error(request, "Por favor selecciona un rango de fechas válido.")
            return redirect('details', id=id)

        # Crear la reserva
        alojamiento = Alojamiento.objects.get(id=alojamiento_id)

        # Verificar si el alojamiento está disponible en las fechas seleccionadas
        if alojamiento.esta_disponible(fecha_inicio, fecha_fin):
            reserva = Reserva.objects.create(
                usuario=request.user,
                paquete=paquete,
                alojamiento=alojamiento,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                precio_total=precio_total
            )
            # Marcar el alojamiento como reservado
            alojamiento.reservado = True
            alojamiento.save()
            # Asociar servicios seleccionados
            for servicio_id in servicios_ids:
                reserva.servicios.add(Servicio.objects.get(id=servicio_id))
            # Enviar correo de confirmación
            enviar_correo_reserva(request.user, reserva)
            return redirect('index')
        else:
            messages.error(request, "El alojamiento no está disponible en esas fechas.")
            return redirect('details', id=id)

    # Filtrar alojamientos disponibles solo si las fechas están definidas
    if 'fecha_inicio' in request.POST and 'fecha_fin' in request.POST:
        for alojamiento in paquete.hospedaje.all():
            if alojamiento.esta_disponible(fecha_inicio, fecha_fin):
                alojamientos_disponibles.append(alojamiento)

    context = {
        'paquete': paquete,
        'alojamientos_disponibles': alojamientos_disponibles,
    }
    return render(request, 'details.html', context)

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
    context = {
        'hospedajes': Alojamiento.objects.all(),
        'servicios': Servicio.objects.all(),
        'paquetes': Paquete.objects.all(),
    }
    
    if request.method == 'POST':
        paquete = Paquete(
            nombre=request.POST.get('nombre'),
            tipo=request.POST.get('tipo'),
            descripcion=request.POST.get('descripcion'),
            imagen=request.FILES.get('imagen'),
        )
        paquete.save()
        
        # Agregar servicios
        servicios = request.POST.getlist('servicios')
        for servicio_id in servicios:
            paquete.servicios.add(servicio_id)  # Agregar ID individualmente
        
        # Agregar hospedajes
        hospedajes = request.POST.getlist('hospedajes')
        for hospedaje_id in hospedajes:
            paquete.hospedaje.add(hospedaje_id)  # Agregar ID individualmente
        
        return redirect('paquetes_admin')
    
    return render(request, 'paquetes_admin.html', context)
#Eliminar paquete
@login_required
def eliminar_paquete(request,id):
    paquete=Paquete.objects.get(nombre=id)
    paquete.delete()
    return redirect(reverse('paquetes_admin'))

#Modificar Paquetes
@login_required
def modificar_paquete(request,id):
    context={
        'paquete':Paquete.objects.get(nombre=id),
        'hospedajes': Alojamiento.objects.all(),
        'servicios': Servicio.objects.all(),
    }
    
    if request.POST.get('hospedajes'):
        paquete=Paquete.objects.get(nombre=id)
        
        hospedajes = request.POST.getlist('hospedajes')
        for hospedaje_id in hospedajes:
            paquete.hospedaje.add(hospedaje_id)
        return redirect('paquetes_admin')
    
    return render(request, 'modificar_paquete.html', context)

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
    return redirect(reverse('alojamiento_admin'))

#Administrar Servicios
@login_required
def servicios_admin(request):
    context={
        'servicios': Servicio.objects.all(),
    }
    if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('precio') and request.POST.get('tipo'):
        servicio=Servicio()
        servicio.nombre=request.POST.get('nombre')
        servicio.descripcion=request.POST.get('descripcion')
        servicio.precio=request.POST.get('precio')
        servicio.tipo=request.POST.get('tipo')
        servicio.save()
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

#Enviar Email
def enviar_correo_reserva(usuario, reserva):
    asunto = f"Confirmación de Reserva: {reserva.paquete.nombre}"
    # Obtener los nombres de los servicios seleccionados
    servicios_seleccionados = reserva.servicios.all()
    servicios_nombres = ", ".join([servicio.nombre for servicio in servicios_seleccionados])  # Formatear como una lista
    mensaje = f"""
    Hola {usuario.username},
    Gracias por realizar una reserva.
    Detalles de tu reserva:
    Id Reservacion: {reserva.id}
    Paquete: {reserva.paquete.nombre}
    Alojamiento: {reserva.alojamiento.nombre}
    Servicios seleccionados: {servicios_nombres}
    Fecha de inicio: {reserva.fecha_inicio}
    Fecha de fin: {reserva.fecha_fin}
    Precio total: ${reserva.precio_total}
    ¡Esperamos que disfrutes de tu estancia!
    Saludos,
    Cuban Pulse.
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email,'programador.ejecutivo.pc@gmail.com']

    send_mail(asunto, mensaje, from_email, recipient_list)