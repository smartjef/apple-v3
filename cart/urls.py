from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detailed/', views.cart_detail, name='cart_detail'),
    path('wish/detailed/', views.wish_detailed, name='wish_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('wish/add/<int:product_id>/', views.wish_add, name='wish_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('wish/remove/<int:product_id>/', views.wish_remove, name='wish_remove'),
    path('shipping/details/', views.shipping_details, name='shipping_details'),
    path('payment/options/', views.payment_options, name='payment_options'),
]
