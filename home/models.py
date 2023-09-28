from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Usuario(AbstractUser):
    departamento = models.CharField(max_length=100, blank=True, null=True)


class Diagnostico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    marca = models.CharField(max_length=50)
    n_serie = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=30)
    diagnostico = models.TextField()
    solucion = models.TextField()
    estado = models.CharField(max_length=20, choices=(('activo', 'activo'), ('en reparacion', 'en reparacion'), ('de vaja', 'de vaja')))
    
    class Meta:
        verbose_name = 'diagnostico'
        verbose_name_plural = 'diagnosticos'


# Función personalizada para obtener la hora actual
def obtener_hora_actual():
    return datetime.now().time()

#El modelo de solicitud
class Solicitud(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    departamento=  models.CharField(max_length=100)
    detalle_equipo= models.CharField(max_length=100)
    descripcion= models.TextField()
    mantenimiento= models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='En espera')
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=obtener_hora_actual)
    #hora = models.TimeField(default=datetime.now().time())
    prioridad = models.CharField(max_length=100, default='Baja')

#modelo de Reporte 
class Reporte(models.Model):
    usuario = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=30)
    departamento = models.CharField(max_length=100)
    servicio_solicitado = models.TextField()
    servicio_realizado = models.CharField(max_length=100)
    observacion = models.TextField()
    tecnico = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=datetime.now().time())
    estado = models.CharField(max_length=20, default='En espera')
    prioridad = models.CharField(max_length=100, default='Baja')

#modelo de Historial
class Historial(models.Model):
    usuario = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=30)
    departamento = models.CharField(max_length=100)
    servicio_solicitado = models.TextField()
    servicio_realizado = models.CharField(max_length=100)
    observacion = models.TextField()
    tecnico = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=datetime.now().time())
    fecha_final = models.DateField(auto_now_add=True)
    hora_final= models.TimeField(default=obtener_hora_actual)
    estado = models.CharField(max_length=20)
    prioridad = models.CharField(max_length=100)
