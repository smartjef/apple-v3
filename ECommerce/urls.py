"""ECommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import ProductSitemap, CategorySitemap, TagSitemap

sitemaps = {
    'categories': CategorySitemap,
    'tags': TagSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('orders.urls', namespace='order')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('', include('root.urls', namespace='root')),
    path('api/', include('api.urls', namespace='api')),
    path('blogs/', include('blogs.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitempas.views.sitemap'),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Apple Master Admin"
admin.site.site_title = "Apple Master Admin"
