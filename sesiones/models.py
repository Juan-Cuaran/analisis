from django.db import models

# Create your models here.
class SesionActiva(models.Model):
    ESTADO = (
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('expirada', 'Expirada'),
    )

    user = models.ForeignKey('autenticacion.User', on_delete=models.CASCADE)
    dispositivo = models.CharField(max_length=255)
    token = models.CharField(max_length=500, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20,choices=ESTADO)
    actividad_progreso = models.BooleanField(default=False)
    ultima_actividad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sesion de {self.user.username} en {self.dispositivo} - Estado: {self.estado}"

class RegistroActividad(models.Model):

    ACTIVIDADES = (
        ('grabacion_video', 'Grabación de video'),
        ('subir_archivo', 'Subir archivo'),
        ('foro', 'Escribir en foro'),
        ('lectura', 'Leer documento'),
        ('ping', 'Ping heartbeat'),
    )

    sesion = models.ForeignKey(SesionActiva, on_delete=models.CASCADE)
    actividad = models.CharField(max_length=255, choices=ACTIVIDADES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sesion} - {self.actividad} - {self.timestamp} "