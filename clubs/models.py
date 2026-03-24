from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    rol_en_club = models.CharField(max_length=50, default='miembro')

class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()
    lugar = models.CharField(max_length=200, blank=True)
    cupo = models.PositiveIntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='eventos/', null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']