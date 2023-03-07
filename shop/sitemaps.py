from django.contrib.sitemaps import Sitemap
from .models import Product, Tag, Category


class CategorySitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return obj.get_absolute_url()

class TagSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return obj.get_absolute_url()

class ProductSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return obj.get_absolute_url()