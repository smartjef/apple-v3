# Create your views here.
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import reverse
from django.views import View
from django.views.decorators.http import require_POST
from cart.forms import CartAddProductForm
from cart.session_info import SessionInfo
from root.breadcrumb import BreadCrumb
from .forms import ReviewForm, SearchForm
from .models import Category, Product, Tag
# Create your views here.


@require_POST
def search_product(request):
    form = SearchForm(data=request.POST)
    search_string = ""
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list')),
        BreadCrumb('Search', None, True)
    ]
    products = None
    if form.is_valid():
        search_string = form.cleaned_data.post('search')
        if search_string:
            products = Product.objects.filter(name__contains=search_string)
    if not products:
        messages.warning(request, "No result matching you query, try and refine you query")

    return render(
        request,
        'shop/product/search.html',
        {
            'products': products,
            'bread_crumb': bread_crumb,
            'search_string': search_string
        }
    )


class ProductsView(View):
    def __init__(self, **kwargs):
        self.request = None
        super().__init__(**kwargs)
        self.categories = Category.objects.all()
        self.products = Product.objects.all()
        self.category = None
        self.tags = Tag.objects.all()
        self._breadCrumb = None
        self.session: SessionInfo = None
        self.paginator: Paginator = None
        self.nav = {"shop": 'active'}

    @property
    def breadCrumb(self):
        self._breadCrumb = [
            BreadCrumb("Home", "/"),
            BreadCrumb("shop", reverse('shop:product_list'), True if not self.category else False)
        ]
        if self.category:
            self._breadCrumb.append(BreadCrumb(str(self.category), self.category.get_absolute_url(), True))
        return self._breadCrumb

    def get(self, request, category_slug=None):
        self.initStates(request, category_slug)
        self.apply_filters()
        return self.render()

    def apply_filters(self):
        filters = self.session.get('filters')
        if filters:
            if self.category_filter:
                self.products = self.products.filter(category__id__in=self.category_filter)
            if self.tag_filters:
                self.products = self.products.filter(tags__id__in=self.tag_filters)
            sort = filters['sort']
            if sort['latest']:
                self.products = self.products.order_by("-updated")
            if sort['popular']:
                # TODO sort by popularity
                pass
            if sort['rating']:
                self.products = self.products.order_by("-rating")

    @property
    def sort_filter(self):
        filters = self.session.get('filters')
        if filters:
            sort = filters['sort']
            return {key: 'checked' for key in sort if sort[key]}

    def post(self, request, category_slug=None):
        """
        Gets filter parameters from user and store them in the session
        """
        self.initStates(request, category_slug)
        sort = self.request.POST.get("sort")
        self.session.add(
            {
                'filters': {
                    'categories': [category.id for category in self.categories if
                                   self.request.POST.get(str(category.slug))],
                    'tags': [tag.id for tag in self.tags if self.request.POST.get(str(tag.slug))],
                    'sort': {'latest': sort == 'latest', 'popular': sort == 'popular', 'rating': sort == 'rating'}
                }
            }
        )
        self.apply_filters()
        # print(self.session.pop('filters'))
        return self.render()

    def render(self):
        return render(
            self.request,
            'shop/product/list-1.html',
            {
                'category': self.category,
                # 'products': self.products,
                'products': self.page,
                'nav': self.nav,
                'bread_crumb': self.breadCrumb,
                'tags': self.tags,
                'tag_filter': self.tag_filters,
                'category_filter': self.category_filter,
                'sort_by': self.sort_filter,
                'title': 'Apple Master Kenya - Shop Our Wide Selection of Computers and Accessories' if not self.category else self.category.name
            }
        )

    @property
    def tag_filters(self):
        filters = self.session.get('filters')
        if filters:
            return filters['tags']

    @property
    def category_filter(self):
        filters = self.session.get('filters')
        if filters:
            return filters['categories']

    def initStates(self, request, slug):
        self.request = request
        self.session = SessionInfo(request)
        if slug:
            self.category = get_object_or_404(Category, slug=slug)
            self.products = self.products.filter(category=self.category)

    @property
    def page(self):
        self.paginator = Paginator(self.products, 6)
        page = self.request.GET.get('page')
        try:
            return self.paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            return self.paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            return self.paginator.page(self.paginator.num_pages)

    @staticmethod
    def validate_number(num):
        if str(num).isdigit() and 2 < int(num) < 20:
            return int(num)
        else:
            return 6


def reset_filters(request):
    session = SessionInfo(request)
    session.clear()
    return redirect('shop:product_list')


def product_list(request, category_slug=None):
    nav = {"shop": 'active'}
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list'), True if not category_slug else False)
    ]
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    tags = Tag.objects.all()

    search = SearchForm(request.GET)
    print(request.GET.get("search"))
    if search.is_valid():
        print("valid form")
        products = products.filter(name=search.cleaned_data["search"])

    sort = request.GET.get("sort")
    if sort == 'latest':
        products = products.order_by("-updated")
    elif sort == 'rating':
        products = products.order_by("-rating")
    paginate = request.GET.get("paginate", 6)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        bread_crumb.append(BreadCrumb(str(category), category.get_absolute_url(), True))

    if request.method == 'POST':
        # category filter
        _categories = []
        for _category in categories:
            if request.POST.get(str(_category.slug)):
                _categories.append(_category)
        if _categories:
            products = products.filter(category__in=_categories)

        # tags filter
        _tags = []
        for tag in tags:
            if request.POST.get(str(tag.slug)):
                _tags.append(tag)
        if _tags:
            products = products.filter(tags__in=_tags)

    paginator = Paginator(products, validate_number(paginate))
    page = request.GET.get('page')
    try:
        products_paged = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products_paged = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products_paged = paginator.page(paginator.num_pages)

    return render(
        request,
        'shop/product/list-1.html',
        {
            'category': category,
            'products': products_paged,
            'nav': nav,
            'bread_crumb': bread_crumb,
            'tags': tags,
            'title': 'Shop',
        }
    )


def validate_number(num):
    if str(num).isdigit() and 2 < int(num) < 20:
        return int(num)
    else:
        return 6


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("shop", reverse('shop:product_list')),
        BreadCrumb(str(product.category), product.category.get_absolute_url()),
        BreadCrumb(str(product), "/", True),
    ]
    cart_product_form = CartAddProductForm()
    if request.method == 'POST':
        f = ReviewForm(request.POST)
        if f.is_valid():
            new_review = f.save(commit=False)
            new_review.user = request.user
            new_review.product = product
            new_review.save()
    form = ReviewForm()
    return render(
        request,
        'shop/product/detail-1.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            "form": form,
            "bread_crumb": bread_crumb,
            'title': product.name,
            'category': product.category,
        }
    )
