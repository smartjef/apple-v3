from django.contrib import admin
from .models import Category, Product, Review, ProductSecondaryImages, Tag

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductSecondaryImagesInline(admin.TabularInline):
    model = ProductSecondaryImages
    raw_id_fields = ['product']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'rating']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSecondaryImagesInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created', 'updated', 'review']
    list_filter = ['user', 'created', 'updated', 'rating', 'product']
    # list_editable = ['rating', 'product']
