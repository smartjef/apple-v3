from datetime import datetime, timedelta
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import reverse
from django.views.decorators.http import require_POST
from accounts.models import Team
from root.breadcrumb import BreadCrumb
from django.db.models import Q
from root.forms import ContactForm
from root.models import FrontDisplayCategory, SubSubscribers
from shop.models import Category, Product, Tag
# Create your views here.


def index(request):
    current_time = datetime.now()
    # Calculate the start and end times for the range of dates to filter
    start_time = current_time - timedelta(days=3)
    end_time = current_time
    bread_crumb = [
        BreadCrumb("Home", "/", True),
    ]
    nav = {"home": 'active'}
    categories = Category.objects.all()
    featured = Product.objects.all()[:8]
    recent = Product.objects.filter(created__range=(start_time, end_time))
    display: list = FrontDisplayCategory.objects.all()
    sliders = None
    brands = None
    tags = Tag.objects.all()
    if len(tags) > 2:
        tags = tags[:4]
    for obj in display:
        if obj.category_name == "Sliders":
            sliders = get_object_or_404(FrontDisplayCategory, category_name="Sliders").displays.all()
        elif obj.category_name == "Brands":
            brands = get_object_or_404(FrontDisplayCategory, category_name="Brands").displays.all()
    return render(
        request,
        "index-1.html",
        {
            "categories": categories,
            "featured": featured,
            "recent": recent,
            "nav": nav,
            "sliders": sliders,
            "brands": brands,
            'tags': tags,
            "bread_crumb": bread_crumb,
            'title': 'Homepage',
        }
    )


@require_POST
def subscribe(request):
    email = request.POST.get("email")
    try:
        SubSubscribers.objects.create(email=email)
        messages.info(request, "Thank you for subscribing")
    except IntegrityError:
        messages.warning(request, "Account is already in our subscription list")

    return redirect('root:index')


def about(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("About", reverse('root:about'), True),
    ]
    nav = {"about": 'active'}
    context= {
        'nav': nav, 
        "bread_crumb": bread_crumb,
        'title': 'About Apple Master Kenya - Your Trusted Provider of Computers and Accessories',
        'teams': Team.objects.all(),
    }
    return render(request, "about-1.html", context)


def contact(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("Contact", reverse('root:contact'), True),
    ]
    nav = {"contact": 'active'}
    form = ContactForm()
    return render(request, "contact-1.html", 
        {
            "form": form, 
            'nav': nav, 
            "bread_crumb": bread_crumb,
            'title': 'Contact Apple Master Kenya - Get in Touch with Us Today',
        }
    )

def advanced_search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'shop/product/list-1.html', {'products': products})

