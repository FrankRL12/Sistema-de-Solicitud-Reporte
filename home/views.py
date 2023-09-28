from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Usuario, Diagnostico, Solicitud, Reporte, Historial
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, Page
from django.contrib import messages
from datetime import datetime
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import logout
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


# Create your views here.



#Vistas para el cliente
def is_superuser(user):
    return user.is_superuser

def inicio(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user)
    return render(request, 'client/inicio.html', {'solicitudes':solicitudes})

#vista para crear la solicitud
def crear_solicitud(request):
    if request.method == 'POST':
        detalle_equipo = request.POST['detalle_equipo']
        descripcion = request.POST['descripcion']
        mantenimiento = request.POST['mantenimiento']
        estado = 'En espera'

        usuario_actual = request.user
        departamento = usuario_actual.departamento
        nombre = usuario_actual.first_name
        apellido = usuario_actual.last_name

        solicitud = Solicitud(usuario=usuario_actual, nombre=nombre, apellido=apellido, departamento=departamento, detalle_equipo=detalle_equipo,
                            descripcion=descripcion, mantenimiento=mantenimiento,  estado=estado)
        solicitud.save()
        return redirect('inicio')
    return render(request, 'client/crear_solicitud.html')

def reporte_client(request):
    reportes = Reporte.objects.filter(usuario=request.user)
    return render(request, 'client/reporte.html', {'reportes':reportes})

#Vista para el historial del usuario.
def historial_cliente(request):
    historiales = Historial.objects.filter(usuario=request.user)

    # Filtro de duración de 24 horas
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    historiales = historiales.filter(fecha__gte=twenty_four_hours_ago)

    # Obtener fechas del formulario de selección
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        historiales = historiales.filter(fecha__range=(start_date, end_date))

    elementos_por_pagina = 2
    paginator = Paginator(historiales, elementos_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'client/historial_cliente.html', {'page_obj': page_obj})

#Vistas para el adminsitrador
@user_passes_test(is_superuser)
def dashboard(request):
    solicitudes = Solicitud.objects.all()

    # Cantidad de elementos por página
    elementos_por_pagina = 2
    paginator = Paginator(solicitudes, elementos_por_pagina)

    # Obtén el número de página desde la URL (por ejemplo, ?page=2)
    page_number = request.GET.get('page')

    # Obtiene la página actual del paginador
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/solicitud/listar_solicitud.html', {'page_obj': page_obj})

def opciones_solicitudes(request, solicitud_id):
    solicitudes = Solicitud.objects.get(id=solicitud_id)

    if request.method == 'POST':
        estado = request.POST.get('estado')
        prioridad= request.POST.get('prioridad')

        solicitudes.estado = estado
        solicitudes.prioridad = prioridad
        solicitudes.save()
        messages.success(request, "Priridades y estados")
        return redirect('dashboard')
    return render(request, 'admin/solicitud/opciones.html', {'solicitudes':solicitudes})

#Vista para crear un reporte
def crear_reporte(request, solicitud_id):
    solicitud = Solicitud.objects.get(id=solicitud_id)

    if request.method == 'POST':
        servicio_realizado = request.POST['servicio_realizado']
        observacion =  request.POST['observacion']
        tecnico = request.POST['tecnico']
        servicio_solicitado = request.POST['servicio_solicitado']

        reporte = Reporte(
            usuario=solicitud.usuario, nombre_completo=f"{solicitud.nombre} {solicitud.apellido}", departamento =solicitud.departamento,
            servicio_solicitado=servicio_solicitado, servicio_realizado= servicio_realizado,
            observacion = observacion, tecnico = tecnico, hora=solicitud.hora, fecha=solicitud.fecha, estado=solicitud.estado,
            prioridad= solicitud.prioridad,
        )
        reporte.save()
        messages.success(request, "reporte Creado")
        # Eliminar la solicitud después de guardar el reporte
        solicitud.delete()
        
        return redirect('reporte')
    return render(request, 'admin/solicitud/crear_reporte.html', {'solicitud': solicitud})

#Listar Reportes
def reporte(request):
    reportes = Reporte.objects.all()

    # Cantidad de elementos por página
    elementos_por_pagina = 2
    paginator = Paginator(reportes, elementos_por_pagina)

    # Obtén el número de página desde la URL (por ejemplo, ?page=2)
    page_number = request.GET.get('page')

    # Obtiene la página actual del paginador
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/report/listar_reportes.html', {'page_obj': page_obj})


def opciones_reportes(request, reporte_id):
    reportes = Reporte.objects.get(id=reporte_id)

    if request.method == 'POST':
        estado = request.POST.get('estado')
        prioridad= request.POST.get('prioridad')

        reportes.estado = estado
        reportes.prioridad = prioridad
        reportes.save()
        messages.success(request, "completado")
        return redirect('reporte')
    return render(request, 'admin/report/opciones_reporte.html', {'reportes':reportes})   

#Vista para usuarios
def usuario(request):
    usuarios = Usuario.objects.all()

    # Cantidad de elementos por página
    elementos_por_pagina = 3
    paginator = Paginator(usuarios, elementos_por_pagina)

    # Obtén el número de página desde la URL (por ejemplo, ?page=2)
    page_number = request.GET.get('page')

    # Obtiene la página actual del paginador
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/usuario/listar_usuario.html', {'page_obj': page_obj})

#Vista para crear Usuarios
def crear_usuario(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        departamento= request.POST.get('departamento')

        usuarios = Usuario(first_name=first_name, last_name=last_name, username=username, password=make_password(password), departamento=departamento)
        usuarios.save()
        messages.success(request, "Usuario Creado")
        return redirect('usuario')
    return render(request, 'admin/usuario/crear_usuario.html')

#Vista para editar un usuario

def editar_usuario(request, usuario_id):
    usuarios = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        departamento= request.POST.get('departamento')

        usuarios.first_name = first_name
        usuarios.last_name = last_name
        usuarios.username = username
        if password:
            usuarios.password = make_password(password)
        usuarios.departamento = departamento
        usuarios.save()
        messages.success(request, "Usuario Editado")
        return redirect('usuario')
    return render(request, 'admin/usuario/editar_usuario.html',{'usuarios': usuarios})

#Vista para eliminar un Usuario
# Define un decorador personalizado para verificar si el usuario es superusuario.
def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Puedes redirigir al usuario a una página de error o realizar otra acción adecuada.
            return HttpResponse("No tienes permiso para eliminar este usuario.")
    return _wrapped_view

# Aplica el decorador a tu vista eliminar_usuario.
@login_required
@superuser_required
def eliminar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        # Verifica si el usuario que intentas eliminar no es el superusuario.
        if not usuario.is_superuser:
            usuario.delete()
            messages.success(request, "Usuario eliminado con éxito.")
        else:
            # Almacena un mensaje de error si se intenta eliminar al superusuario.
            messages.error(request, "No puedes eliminar al superusuario.")
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")

    return redirect('/usuario/')  # Puedes cambiar la URL de redirección según sea necesario.



def equipo(request):
    return render(request, 'admin/equipo/listar_equipo.html')


#Vistas para el diagnosticos
def diagnostico(request):

    if request.method == 'POST':
        # Aquí manejas la creación de un nuevo diagnóstico
        nombre = request.POST['nombre']
        marca = request.POST['marca']
        n_serie = request.POST['n_serie']
        modelo = request.POST['modelo']
        ubicacion = request.POST['ubicacion']
        diagnostico = request.POST['diagnostico']
        solucion = request.POST['solucion']
        estado = request.POST['estado']
        agregar_diagnostico = Diagnostico(nombre=nombre, marca=marca, n_serie=n_serie,
                                          modelo=modelo, ubicacion=ubicacion, diagnostico=diagnostico,
                                          solucion=solucion, estado=estado)
        agregar_diagnostico.save()
        messages.success(request, "Diagnostico Creado")
        return redirect('diagnostico')  # Redirige a la lista de diagnósticos después de crear uno nuevo
    else:
        # Aquí manejas la lista de diagnósticos
        diagnosticos = Diagnostico.objects.all()
        elementos_por_pagina = 3
        paginator = Paginator(diagnosticos, elementos_por_pagina)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/diagnostico/listar_diagnostico.html', {'page_obj': page_obj})



def editar_diagnostico(request, diagnostico_id):
    diagnost =Diagnostico.objects.get(id=diagnostico_id)

    if request.method == 'POST':
        nombre=request.POST['nombre']
        marca=request.POST['marca']
        n_serie=request.POST['n_serie']
        modelo=request.POST['modelo']
        ubicacion=request.POST['ubicacion']
        diagnostico=request.POST['diagnostico']
        solucion=request.POST['solucion']
        estado=request.POST['estado']

        diagnost.nombre=nombre
        diagnost.marca=marca
        diagnost.n_serie=n_serie
        diagnost.modelo=modelo
        diagnost.ubicacion=ubicacion
        diagnost.diagnostico=diagnostico
        diagnost.solucion=solucion
        diagnost.estado=estado

        diagnost.save()
        messages.success(request, "Diagnostico Editado")
        return redirect('diagnostico')
    return render(request, 'admin/diagnostico/modal_editar.html', {'diagnost':diagnost})

#Vista para actualizar el diagnostico

#Vista para eliminar un diagnostico
def eliminar_diagnostico(request, diagnosticos_id):
	diagnosticos = get_object_or_404(Diagnostico, id=diagnosticos_id)
	diagnosticos.delete()
	return redirect('/diagnostico/')

#Vista para el historial.
def historial(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        historiales = Historial.objects.filter(fecha__range=(start_date, end_date))
    else:
        historiales = Historial.objects.all()

    elementos_por_pagina = 2
    paginator = Paginator(historiales, elementos_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasar las fechas seleccionadas a la plantilla
    return render(request, 'admin/historial/listar_historial.html', {
        'page_obj': page_obj,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })

#Vista para mover a historial
def move_historial(request, reporte_id):
    try:
        # Obtener el objeto Reporte
        reporte = Reporte.objects.get(id=reporte_id)

        # Crear una instancia de Historial con los atributos de Reporte
        historial = Historial(
            usuario=reporte.usuario,
            nombre_completo=reporte.nombre_completo,
            departamento=reporte.departamento,
            servicio_solicitado=reporte.servicio_solicitado,
            servicio_realizado=reporte.servicio_realizado,
            observacion=reporte.observacion,
            tecnico=reporte.tecnico,
            fecha=reporte.fecha,
            hora=reporte.hora,
            fecha_final=datetime.now().date(),
            hora_final=datetime.now().time(),
            estado=reporte.estado,
            prioridad=reporte.prioridad
        )

        # Guardar la instancia de Historial en la base de datos
        historial.save()

        # Eliminar el objeto Reporte original
        reporte.delete()

        # Redirigir al usuario a la vista de reportes (ajusta la URL según tu configuración)
        return redirect('reporte')

    except Reporte.DoesNotExist:
        return HttpResponse("El reporte no existe.")
    
#Para generar el PDF de Historial
def generar_pdf(request, historial_id):
    historial = get_object_or_404(Historial, pk=historial_id)
    template_path = 'pdf_template.html'
    context = {'historial': historial}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = f'attachment; filename="historial_{historial.id}.pdf"'

    template = render_to_string(template_path, context)
    # Create a PDF object, and render the template content into the PDF file
    pisa_status = pisa.CreatePDF(template, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

#vista para generar el PDF de dignostico
def diagnostico_pdf(request, diagnosticos_id):
    diagnosticos = get_object_or_404(Diagnostico, pk=diagnosticos_id)
    template_path = 'pdf_diagnostico.html'
    context = {'diagnosticos': diagnosticos}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = f'attachment; filename="diagnostico_{diagnosticos.id}.pdf"'

    template = render_to_string(template_path, context)
    # Create a PDF object, and render the template content into the PDF file
    pisa_status = pisa.CreatePDF(template, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response


#Vista para el sierre de ccion en django
def historial_por_rango(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        historiales = Historial.objects.filter(
            Q(fecha__range=[fecha_inicio, fecha_fin]) |
            Q(fecha_final__range=[fecha_inicio, fecha_fin])
        )

        return render(request, 'admin/historial/consulta_por_fechas.html', {'historiales': historiales})

    return render(request, 'admin/historial/formulario_consulta.html')