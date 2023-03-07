import os
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

CATEGORY_IMAGES_PATH = os.path.join("uploads", "shop", "category")
PRODUCTS_IMAGES_PATH = os.path.join("uploads", "shop", "products", "primary")
PRODUCTS_SECONDARY_IMAGES_PATH = os.path.join("uploads", "shop", "products", "secondary")
TAGS_IMAGES_PATH = os.path.join("uploads", "shop", "tags")
RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]
# Create your models here.

def category_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.slug, instance.id, ext)
    return os.path.join(CATEGORY_IMAGES_PATH, filename)


def product_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s.%s" % (instance.slug, instance.id, instance.category.slug, ext)
    return os.path.join(PRODUCTS_IMAGES_PATH, filename)


def product_secondary_image_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.product.slug, instance.id, ext)
    return os.path.join(PRODUCTS_SECONDARY_IMAGES_PATH, filename)


def tag_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.slug, instance.id, ext)
    return os.path.join(TAGS_IMAGES_PATH, filename)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to=category_file_name,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug]
        )


class Tag(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to=tag_file_name,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug]
        )

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    tags = models.ManyToManyField(Tag, related_name="products")
    image = models.ImageField(
        upload_to=product_file_name,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    additional_info = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=4
    )

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_discount(self, rate=25):
        return "%.2f" % (self.price * Decimal((100 + rate) / 100))

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            args=[self.id, self.slug]
        )

    def iter_full_stars(self) -> range:
        return range(int(str(self.rating)))

    def iter_empty_stars(self) -> range:
        return range(len(self.iter_full_stars()), 5)


class ProductSecondaryImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="secondary_images")
    image = models.ImageField(
        upload_to=product_secondary_image_name,
        blank=False,
        null=False,
    )


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=4
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    review = models.TextField()
