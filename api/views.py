import datetime
import statistics

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from payment.models import Payment, Transaction
from shop.models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, AllProductsSerializer, \
    OrderSerializer, PaymentSerializer

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewsListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewsDetailView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class AllProductsView(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = AllProductsSerializer

    def get_queryset(self):
        return Category.objects.all()


class CategoryAddView(generics.ListCreateAPIView):
    """
    Implements both get and post for you and adds the new object
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CategoryAdd(APIView):
    """
      The base abstract class, you have to implement post, get, put, delete methods
    """

    def post(self, request):
        """
        Response is given a serializable data/dictionary
        """
        print(request.POST["name"])
        return Response({"hellow": "world"})

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(instance=categories, many=True)
        return Response(serializer.data)


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderHistoryListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.request.user.order.all()


class OrderDetailedView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class MpesaPaymentView(APIView):
    def post(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        data = JSONParser().parse(request)
        stk_callback = data["Body"]["stkCallback"]
        if not stk_callback.get("MerchantRequestID") or not stk_callback.get("CheckoutRequestID"):
            return Response({"error": "Invalid Input data"}, status=404)
        new_payment = Payment(
            order=order,
            merchant_request_id=stk_callback.get("MerchantRequestID"),
            checkout_request_id=stk_callback.get("CheckoutRequestID"),
            result_code=stk_callback.get("ResultCode"),
            result_description=stk_callback.get("ResultDesc"),
        )
        new_payment.save()
        meta = stk_callback.get("CallbackMetadata")
        if meta:
            payment_detail = Transaction(payment=new_payment, amount=0)
            payment_detail.save()
            for item in meta.get("Item"):
                if item.get("Name") == 'Amount':
                    payment_detail.amount = float(item.get('Value'))
                elif item.get("Name") == 'MpesaReceiptNumber':
                    payment_detail.mpesa_receipt_number = item.get('Value')
                elif item.get("Name") == 'TransactionDate':
                    payment_detail.transaction_date = item.get('Value')
                elif item.get("Name") == 'PhoneNumber':
                    payment_detail.phone_number = item.get('Value')
            payment_detail.save()
            # _order = payment_detail.payment.order
            # if not _order.paid:
            #     paid = _order.get_amount_paid()
            #     if paid >= _order.get_total_cost():
            #         _order.paid = True
            #         _order.save()
        return Response({"Ack": "Thanks received", "body": data})

    # pay = {}
    # for item in meta.get("Item"):
    #     if item.get("Name") == 'Amount':
    #         pay['amount'] = float(item.get('Value'))
    #     elif item.get("Name") == 'MpesaReceiptNumber':
    #         pay['mpesa_receipt_number'] = item.get('Value')
    #     elif item.get("Name") == 'TransactionDate':
    #         pay['transaction_date'] = item.get('Value')
    #     elif item.get("Name") == 'PhoneNumber':
    #         pay['phone_number'] = item.get('Value')
    # if pay:
    #     PaymentDetails.objects.create(
    #
    #     )


class PaymentView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('created')


class MonthlySalesView(APIView):
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # orders = Order.objects.filter(paid=True)
        orders = Order.objects.all()
        monthly_sales = []
        curr_month = datetime.datetime.now().month
        for month in range(1, curr_month + 1):
            monthly_orders = orders.filter(created__month=month)
            if len(monthly_orders):
                monthly_sales.append(
                    {
                        'x': MONTHS[month - 1],
                        'y': statistics.mean(
                            [order.get_amount_paid() for order in monthly_orders])
                    }
                )
            else:
                monthly_sales.append(
                    {
                        'x': MONTHS[month - 1],
                        'y': 0
                    }
                )
        context = {
            'sales': sum([order.get_amount_paid() for order in orders]),
            'monthly_sales': monthly_sales,
            'orders': len(orders),
            'payments': sum([len(order.payment.all()) for order in orders]),
            'growth': 23
        }

        return Response(context)
