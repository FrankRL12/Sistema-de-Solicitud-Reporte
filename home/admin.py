from django.contrib import admin
from .models import Usuario, Diagnostico, Solicitud, Reporte, Historial


# Register your models here.
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre', 'marca', 'n_serie', 'modelo', 'ubicacion', 'diagnostico', 'solucion', 'estado')

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('usuario','nombre', 'apellido', 'departamento', 'detalle_equipo', 'descripcion',
                    'mantenimiento', 'estado', 'fecha', 'hora', 'prioridad')

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_completo','departamento','servicio_solicitado',
                    'servicio_realizado', 'observacion', 'tecnico', 'fecha', 'hora', 'estado', 'prioridad')
    
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('usuario','nombre_completo', 'departamento','servicio_solicitado',
                    'servicio_realizado', 'observacion', 'tecnico', 'fecha', 'hora','fecha_final', 'hora_final', 'estado', 'prioridad')

admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(Usuario)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Historial, HistorialAdmin)
