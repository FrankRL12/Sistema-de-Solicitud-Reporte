from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView




def is_superuser(user):
    return user.is_superuser

urlpatterns = [
    #Urls para el cliente
    path('',LoginView.as_view(template_name='client/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='client/logout.html'), name='logout'),
    path('inicio/',login_required(views.inicio), name='inicio'),
    path('crear_solicitud/', login_required(views.crear_solicitud), name='crear_solicitud'),
    path('reporte_client/',login_required(views.reporte_client), name='reporte_client'),
    path('historial_cliente/',login_required(views.historial_cliente), name='historial_cliente'),

    #Urls para el admin
    #Urls de Solicitudes
    path('dashboard/', user_passes_test(is_superuser)(views.dashboard), name='dashboard'),
    path('opciones_solicitudes/<int:solicitud_id>', user_passes_test(is_superuser)(views.opciones_solicitudes), name='opciones_solicitudes'),
    path('crear_reporte/<int:solicitud_id>',user_passes_test(is_superuser)(views.crear_reporte), name='crear_reporte'),
    path('equipo/',user_passes_test(is_superuser)(views.equipo), name='equipo'),

    path('logout/',LogoutView.as_view(template_name='admin/log/login.html'), name='logout'),

    #urls de diagnosticos
    path('diagnostico/',user_passes_test(is_superuser)(views.diagnostico), name='diagnostico'),
    #path('agregar_diagnostico/',user_passes_test(is_superuser)(views.agregar_diagnostico), name='agregar_diagnostico'),
    path('eliminar_diagnostico/<int:diagnosticos_id>',user_passes_test(is_superuser)(views.eliminar_diagnostico), name='eliminar_diagnostico'),
    path('editar_diagnostico/<int:diagnostico_id>',user_passes_test(is_superuser)(views.editar_diagnostico), name='editar_diagnostico'),
    
    #Urls de Historial
    path('move_historial/<int:reporte_id>',user_passes_test(is_superuser)(views.move_historial), name='move_historial'),
    path('historial/',user_passes_test(is_superuser)(views.historial), name='historial'),

    #Urls de reportes
    path('reporte/',user_passes_test(is_superuser)(views.reporte), name='reporte'),
    path('opciones_reportes/<int:reporte_id>', user_passes_test(is_superuser)(views.opciones_reportes), name='opciones_reportes'),

    #Urls de Usuarios
    path('usuario/',user_passes_test(is_superuser)(views.usuario), name='usuario'),
    path('crear_usuario/',user_passes_test(is_superuser)(views.crear_usuario), name='crear_usuario'),
    path('editar_usuario/<int:usuario_id>',user_passes_test(is_superuser)(views.editar_usuario), name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>',user_passes_test(is_superuser)(views.eliminar_usuario), name='eliminar_usuario'),

    #Para generar el PDF
    #path('generar_pdf/<int:historial_id>',user_passes_test(is_superuser)(views.generar_pdf), name='generar_pdf'),
    #path('diagnostico_pdf/<int:diagnosticos_id>',user_passes_test(is_superuser)(views.diagnostico_pdf), name='diagnostico_pdf'),
    path('generar_pdf/<int:historial_id>',views.generar_pdf, name='generar_pdf'),
    path('diagnostico_pdf/<int:diagnosticos_id>',views.diagnostico_pdf, name='diagnostico_pdf'),
]
