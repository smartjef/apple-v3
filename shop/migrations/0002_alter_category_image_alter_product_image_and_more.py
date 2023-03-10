# Generated by Django 4.0.8 on 2022-12-10 13:31

from django.db import migrations
import django_resized.forms
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[100, 100], upload_to=shop.models.category_file_name),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to=shop.models.product_file_name),
        ),
        migrations.AlterField(
            model_name='productsecondaryimages',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to=shop.models.product_secondary_image_name),
        ),
        migrations.AlterField(
            model_name='tag',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[430, 1000], upload_to=shop.models.tag_file_name),
        ),
    ]
