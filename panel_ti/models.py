from django.db import models

# Create your models here.
class PoliticaSesion(models.Model):
    modificado_por = models.ForeignKey('autenticacion.User', on_delete=models.SET_NULL, null=True)
    limite_sesiones = models.IntegerField(default=3)
    tiempo_inactividad = models.IntegerField(default=5)  # en minutos
    tiempo_expiracion = models.IntegerField(default=10)  # en minutos
    tiempo_preservacion = models.IntegerField(default=5)  # en minutos
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Política de sesión para {self.modificado_por.username} - Límite: {self.limite_sesiones}"
    
class Auditoria(models.Model):
    usuario = models.ForeignKey('autenticacion.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    acciones_modificads = models.TextField()
    valor_anterior = models.TextField()
    valor_nuevo = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - {self.acciones_modificads} - {self.timestamp}"