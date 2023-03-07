from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.ProductsView.as_view(), name='product_list'),
    path('search/', views.search_product, name='search'),
    path('filters/reset/', views.reset_filters, name='reset_filters'),
    # path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.ProductsView.as_view(), name='product_list_by_category'),
    # path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:product_id>/<slug:slug>/', views.product_detail, name='product_detail'),
]