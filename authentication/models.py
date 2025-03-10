from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Replace ImageField with URLField or CharField
    profile_picture_url = models.URLField(max_length=255, blank=True, null=True)  # Store image URL instead of actual image
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

# Sinal para criar automaticamente um perfil ao criar um usuário
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Se você quiser registrar esse modelo no admin, adicione ao admin.py:
# from .models import UserProfile
# admin.site.register(UserProfile)
