import os
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from phone_field.models import PhoneField

# Create your models here.
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.id, instance.title, ext)
    if instance.category.category_name == "Sliders":
        return os.path.join('uploads', "display", "sliders", filename)
    else:
        return os.path.join('uploads', "display", "vendors", filename)


def logo_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % ("logo", instance.id, ext)
    return os.path.join("uploads", "logo", filename)


class ContactInfo(models.Model):
    organization_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = PhoneNumberField()
    about_us = models.TextField(blank=True, null=True)
    street = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    twitter_handle = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linked_in = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    logo = models.ImageField(
        upload_to=logo_filename,
        blank=False,
        null=False,
    )

    def getAddress(self):
        return f"{self.street} {self.zip_code} {self.city}, {self.country}"


class FrontDisplayCategory(models.Model):
    category_name = models.CharField(
        db_index=True,
        max_length=50,
        unique=True,
        choices=(
            ("Sliders", "Sliders"),
            ("Brands", "Brands")
        )
    )

    def __str__(self):
        return self.category_name


class FrontDisplay(models.Model):
    category = models.ForeignKey(FrontDisplayCategory, on_delete=models.CASCADE, related_name="displays")
    title = models.CharField(max_length=50)
    description = models.CharField(null=True, blank=True, max_length=150)
    image = models.ImageField(
        upload_to=content_file_name,
        blank=False,
        null=False
    )


class SubSubscribers(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

