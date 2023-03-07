from django.conf import settings
from shop.models import Product

class WishList:
    def __init__(self, request):
        self.session = request.session
        wish = self.session.get(settings.WISH_LIST_SESSION_ID)
        if not wish:
            wish = self.session[settings.WISH_LIST_SESSION_ID] = {}
        self.wish = wish

    def add(self, product: Product):
        product_id = str(product.id)
        if product_id not in self.wish:
            self.wish[product_id] = {
            }
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.wish:
            del self.wish[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.wish.keys()
        prod = Product.objects.filter(id__in=product_ids)
        wish = self.wish.copy()
        for pro in prod:
            wish[str(pro.id)]['product'] = pro
        for item in wish.values():
            yield item

    def __len__(self):
        return sum(1 for item in self.wish.values())

    def clear(self):
        del self.session[settings.WISH_LIST_SESSION_ID]
        self.save()

    def __str__(self):
        return str(self.wish)
