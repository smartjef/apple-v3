from django.contrib import admin
from .models import ContactInfo, FrontDisplayCategory, FrontDisplay, SubSubscribers
# Register your models here.

@admin.register(ContactInfo)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["organization_name", "email", "phone_number", "country", "zip_code",
                    "twitter_handle", "facebook", "linked_in", "instagram"]


class DisplayItemsInline(admin.TabularInline):
    model = FrontDisplay
    raw_id_fields = ['category']


@admin.register(FrontDisplayCategory)
class FrontDisplayCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    list_filter = ['category_name']
    inlines = [DisplayItemsInline]


@admin.register(SubSubscribers)
class SubSubscribersAdmin(admin.ModelAdmin):
    list_display = ('email', 'created', 'is_subscribed')
    list_filter = ('created', 'is_subscribed')
    search_fields = ('email',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    list_editable = ('is_subscribed',)
