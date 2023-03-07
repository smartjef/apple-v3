from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import UserProfile
from orders.models import Order, OrderItem
from payment.models import Transaction, Payment
from shop.models import Category, Product, Review


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', "first_name", "last_name", "userprofile"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class AllProductsSerializer(serializers.ModelSerializer):
    # try commending this it will bring the ids of the product
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        # fields = "__all__"
        fields = ['name', 'slug', 'image', 'products']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderDetail(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class PaymentDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    items = PaymentDetailedSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
