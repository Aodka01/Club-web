from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    carrera = models.CharField(max_length=100, blank=True)
    semestre = models.PositiveIntegerField(null=True, blank=True)
    area_maestro = models.CharField(max_length=100, blank=True, verbose_name="Área de maestro")

    def __str__(self):
        return f'{self.user.username} Profile'

