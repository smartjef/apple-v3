from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('', views.make_manual_payment, name='make_manual_payment'),
    path('<int:order_id>/invoice', views.view_invoice, name='order_invoice'),
    path('<int:order_id>/transact/', views.create_transaction, name='create_transaction'),
    path('<int:order_id>/payment/', views.make_payment, name='make_payment'),
    path('<int:order_id>/payment/transactions/', views.order_payment_history, name='order_payment_history'),
]
