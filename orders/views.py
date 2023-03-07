from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import reverse

from cart.cart_wish import CartWish
from orders.models import OrderItem, Order
from root.breadcrumb import BreadCrumb


# Create your views here.


def order_create(request):
    cart = CartWish(request)
    if cart.length_cart():
        order = Order.objects.create(user=request.user)
        for item in cart.iter_cart():
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        # clear the cart
        cart.clear_cart()
        messages.success(request, f"Your New order ORD-{order.created.year}-{order.id} created successfully!"
                                  f"We will get back to you soon")
        # TODO NOTIFY ADMINS AND SEND INVOICE TO USER
        return redirect(
            reverse('order:order_details', args=[order.id])
        )
    return redirect('shop:product_list')


@login_required
def order_history(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("Shop", reverse('shop:product_list')),
        BreadCrumb("Orders", reverse('order:order_history'), True),
    ]
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/order_history.html', {'orders': orders, 'bread_crumb': bread_crumb})


@login_required
def view_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("Shop", reverse('shop:product_list')),
        BreadCrumb("Orders", reverse('order:order_history')),
        BreadCrumb(f"ORD-{order_id}", reverse('order:order_details', args=[order_id]), True),
    ]
    return render(request, 'order/order_details.html', {"order": order, "bread_crumb": bread_crumb})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
