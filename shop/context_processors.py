from .models import Category, Product
from .forms import SearchForm

def product_category(request):
    return {'categories': Category.objects.all()}

def search_form(request):
    return {'search_form': SearchForm()}

def products(request):
    return {'products':Product.objects.all()[:5]}
