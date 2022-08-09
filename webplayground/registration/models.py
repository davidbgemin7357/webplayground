from django.db import models
from django.contrib.auth.models import User

# decorador para las señales
from django.dispatch import receiver
from django.db.models.signals import post_save

# función para upload_to, hará que el avatar antiguo se elimine y solo se conserve el más reciente.
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # cambiar profiles por la función creada custom_upload_to
    # avatar = models.ImageField(upload_to='profiles', null=True, blank=True)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']


# señales: función que ejecuta un código en un momento determinado de la vida de una instancia, sea antes de guardarla o después o antes o después de eliminarla
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    # si se guarda por primera vez
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print('Se acaba de crear un usuario y su perfil enlazado')