# Generated by Django 4.0.8 on 2022-12-10 13:31

from django.db import migrations
import django_resized.forms
import root.models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='logo',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to=root.models.logo_filename),
        ),
        migrations.AlterField(
            model_name='frontdisplay',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[150, 150], upload_to=root.models.content_file_name),
        ),
    ]
