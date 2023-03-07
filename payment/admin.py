from django.contrib import admin

from .models import Payment, Transaction


# Register your models here.


class TransactionInline(admin.TabularInline):
    model = Transaction
    row_id_field = [
        "payment"
    ]
    fields = [
        "merchant_request_id", "checkout_request_id",
        "result_code", "mpesa_receipt_number",
        "transaction_date", "phone_number", "amount"
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["order", "created", "completed"]
    list_filter = ["created"]
    inlines = [TransactionInline]
