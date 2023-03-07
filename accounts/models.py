import os
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.user.first_name, ext)
    return os.path.join('uploads', "profile", filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    image = ResizedImageField(
        upload_to=content_file_name,
        blank=True,
        null=False,
        size=[500, 500]
    )
    phone = PhoneNumberField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile...'

class ResidentialInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='residentialinfo')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zip_code = models.PositiveIntegerField(null=True, blank=True)
    apartment_or_floor = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, choices=(
        ("Kenya", "Kenya"),
        ("Rwanda", "Rwanda"),
        ("Uganda", "Uganda"),
        ("Tanzania", "Tanzania"),
        ("Sudan", "Sudan"),
    ))
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    def get_address(self):
        return f"{self.address} {self.zip_code} {self.city}, {self.country}"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_residential_ifo(sender, instance, created, **kwargd):
    if created:
        ResidentialInfo.objects.create(user=instance)

class Team(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='teams/')
    order = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-order',)
        
    def __str__(self):
        return self.user.username