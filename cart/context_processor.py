from .cart_wish import CartWish

def wish_cart(request):
    return {'cart_wish': CartWish(request)}
