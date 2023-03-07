from decimal import Decimal
from django.conf import settings
from shop.models import Product


class CartWish:
    def __init__(self, request):
        self.session = request.session
        cart_wish = self.session.get(settings.CART_SESSION_ID)
        if not cart_wish:
            cart_wish = self.session[settings.CART_SESSION_ID] = {
                settings.CART_ITEMS: {},
                settings.WISH_ITEMS: {},
            }
        # form aliases of cart items and wish items
        self.cart_items = cart_wish[settings.CART_ITEMS]
        self.wish_items = cart_wish[settings.WISH_ITEMS]
        self.cart_wish = cart_wish

    def add_to_cart(self, product: Product, quantity: int = 1, override_quantity: bool = False):
        if settings.CART_ITEMS not in self.cart_wish:
            self.cart_wish[settings.CART_ITEMS] = {}
            self.cart_items = self.cart_wish[settings.CART_ITEMS]
        product_id = str(product.id)
        if product_id not in self.cart_items:
            self.cart_items[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart_items[product_id]['quantity'] = quantity
        else:
            self.cart_items[product_id]['quantity'] += quantity
        self.save()

    def add_to_wish(self, product: Product):
        if settings.WISH_ITEMS not in self.cart_wish:
            self.cart_wish[settings.WISH_ITEMS] = {}
            self.wish_items = self.cart_wish[settings.WISH_ITEMS]
        product_id = str(product.id)
        if product_id not in self.wish_items:
            self.wish_items[product_id] = {
            }
        self.save()

    def save(self):
        self.session.modified = True

    def remove_from_cart(self, product):
        product_id = str(product.id)
        if product_id in self.cart_items:
            del self.cart_items[product_id]
            self.save()

    def remove_from_wish(self, product):
        product_id = str(product.id)
        if product_id in self.wish_items:
            del self.wish_items[product_id]
            self.save()

    def iter_cart(self):
        product_ids = self.cart_items.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = self.cart_items.copy()
        for product in products:
            cart_items[str(product.id)]['product'] = product
        for item in cart_items.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def iter_wish(self):
        product_ids = self.wish_items.keys()
        prod = Product.objects.filter(id__in=product_ids)
        wish_items = self.wish_items.copy()
        for pro in prod:
            wish_items[str(pro.id)]['product'] = pro
        for item in wish_items.values():
            yield item

    def length_cart(self):
        return sum(item['quantity'] for item in self.cart_items.values())

    def length_wish(self):
        return sum(1 for _ in self.wish_items.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart_items.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def clear_cart(self):
        self.cart_items.clear()
        self.save()

    def clear_wish(self):
        self.wish_items.clear()
        self.save()

    def __str__(self):
        return str(self.cart_wish)

    def __repr__(self):
        return self.__str__()
