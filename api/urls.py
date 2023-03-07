from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
    # path('category/', views.CategoryListView.as_view(), name='categories_list'),
    path('category/', views.CategoryAddView.as_view(), name='categories_list'),
    # path('category/', views.CategoryAddView.as_view(), name='categories_list'),
    # path('category/', views.CategoryAdd.as_view(), name='categories_list'),
    # path('category/<int:pk>', views.CategoryDetailView.as_view(), name='categories_detail'),
    path('category/<int:pk>', views.CategoryRetrieveUpdateDestroy.as_view(), name='categories_detail'),
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='products_detail'),
    path('reviews/', views.ReviewsListView.as_view(), name='reviews_list'),
    path('reviews/<int:pk>', views.ReviewsDetailView.as_view(), name='reviews_detail'),
    path('', views.AllProductsView.as_view(), name='shop'),
    path('order/history/', views.OrderHistoryListView.as_view(), name='order_history'),
    path('order/<int:pk>/', views.OrderDetailedView.as_view(), name='order_detail'),
    path('order/<int:pk>/pay/', views.MpesaPaymentView.as_view(), name='order_payment'),
    path('report/revenue/', views.PaymentView.as_view(), name='revenue'),
    path('revenue/', views.MonthlySalesView.as_view(), name='test_revenue'),
]
