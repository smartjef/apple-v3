from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import reverse
from django.views.decorators.http import require_POST
from root.breadcrumb import BreadCrumb
from .cart_wish import CartWish
from .forms import CartAddProductForm, CreditCardForm, CartAddSingleProduct
from accounts.forms import ResidentialInfoForm, UserEditForm, UserProfileInfo
from shop.models import Product


@require_POST
def cart_add(request, product_id):
    cart = CartWish(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    # print(form)
    if form.is_valid():
        cd = form.cleaned_data
        cd['quantity_fake'] = cd['quantity']
        cart.add_to_cart(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    else:
        print("ERROR IN VALIDATION")
    cart.remove_from_wish(product)
    return redirect('cart:cart_detail')


def wish_add(request, product_id):
    wish = CartWish(request)
    product = get_object_or_404(Product, id=product_id)
    wish.add_to_wish(product=product)
    return redirect('cart:wish_detail')


@require_POST
def cart_remove(request, product_id):
    cart = CartWish(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_from_cart(product)
    return redirect('cart:cart_detail')


def wish_remove(request, product_id):
    wish = CartWish(request)
    product = get_object_or_404(Product, id=product_id)
    wish.remove_from_wish(product)
    return redirect('cart:wish_detail')


def cart_detail(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list')),
        BreadCrumb("cart", reverse("cart:cart_detail"), True),
    ]
    cart = CartWish(request)
    for item in cart.iter_cart():
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail-1.html', {'bread_crumb': bread_crumb, 'title': 'Shopping Cart',})


def wish_detailed(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list')),
        BreadCrumb("Wish list", reverse("cart:wish_detail"), True),
    ]

    return render(request, 'cart/wish_detailed-1.html',
                  {'hidden_form': CartAddSingleProduct(), "bread_crumb": bread_crumb})


@login_required
def shipping_details(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list')),
        BreadCrumb("cart", reverse("cart:cart_detail")),
        BreadCrumb("Shipping details", reverse("cart:shipping_details"), True),
    ]

    user_form = UserEditForm(instance=request.user)
    profile_form = UserProfileInfo(instance=request.user.userprofile)
    residential_info_form = ResidentialInfoForm(instance=request.user.residentialinfo)

    if request.method == 'POST':
        residential_info_form = ResidentialInfoForm(data=request.POST, instance=request.user.residentialinfo)
        profile_form = UserProfileInfo(data=request.POST, instance=request.user.userprofile)
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if residential_info_form.is_valid() and profile_form.is_valid() and user_form.is_valid():
            residential_info_form.save()
            profile_form.save()
            user_form.save()
            return redirect('order:order_create')

    return render(request, 'cart/shipping_details.html',
                  {'residential_info_form': residential_info_form, 'user_form': user_form,
                   'profile_form': profile_form, 'bread_crumb': bread_crumb})


@login_required
def payment_options(request):
    # TODO REMOVED SO WORK ON IT LATER
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list')),
        BreadCrumb("cart", reverse("cart:cart_detail")),
        BreadCrumb("Shipping details", reverse("cart:shipping_details")),
        BreadCrumb("Payment ptions", reverse("cart:payment_options"), True),
    ]
    card_form = CreditCardForm()
    return render(request, 'cart/payment_options.html', {'card_form': card_form, 'bread_crumb': bread_crumb})
