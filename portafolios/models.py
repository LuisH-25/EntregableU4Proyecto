from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Portafolio(models.Model):
    foto = models.CharField(max_length=400)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # si no pasa nada, por defecto estara vacio
    tags = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)   # anhade la fecha por defecto
    datecompleted = models.DateTimeField(null=True, blank=True)     # inicialmente es null, se acepta vacio
    private = models.BooleanField(default=False)    # por defecto es publico
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # si se elimina el usuario, se elimina las tareas

    def __str__(self):
        return self.title + " -by " + self.user.username

    class Meta:
        db_table = "portafolios"

class UsuarioIp(models.Model):
    ip_login = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip_login + " -by " + self.user.username

    class Meta:
        db_table = "ips_listado"