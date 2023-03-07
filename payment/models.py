from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order


# Create your models here.


class Payment(models.Model):
    order = models.OneToOneField(Order, related_name="payment", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_amount_paid(self):
        return sum([transaction.amount for transaction in self.transactions.all()])

    def __str__(self):
        return f"{self.order}'s Payment"


class Transaction(models.Model):
    payment = models.ForeignKey(Payment, related_name='transactions', on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.IntegerField()
    result_description = models.TextField()
    mpesa_receipt_number = models.CharField(max_length=100, null=True, blank=True)
    transaction_date = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    created = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(order=instance)


@receiver(post_save, sender=Transaction)
def check_if_payment_complete_and_mark_paid(sender, instance, created, **kwargs):
    if created:
        # update order payment status to true if balance is o
        _order = instance.payment.order
        _payment = _order.payment
        if _order.get_balance() <= 0.95:
            _payment.completed = True
            _payment.save()
        else:
            _payment.completed = False
            _payment.save()
