from django.shortcuts import render, get_object_or_404
from .models import Product, Variation
from category.models import Category
from cart.models import CartItem
from cart.views import _get_cart_id
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
# Create your views here.

def store_view(request, category_slug = None):
    """"""
    categories = None
    search_category = None
    products = None
    no_of_items = 0

    categories = Category.objects.all()

    if category_slug != None:
        search_category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(is_avail = True, category = search_category).order_by('id')

    else:
        products = Product.objects.filter(is_avail = True).order_by('id')

    paginator = Paginator(products, 6)
    page  = request.GET.get('page')
    page_products = paginator.get_page(page)
    # if page == None:
    #     page_products = products
    # print(page)

    no_of_items = len(products)

    context = {
        'categories': categories,
        'products' : page_products,
        "no_of_items": no_of_items,
    }

    return render(request, 'store/store.html', context)

def product_view(request, product_id = None):
    """"""
    try:
        product = get_object_or_404(Product,  pk = product_id)
        product_variations = Variation.objects.filter(product = product)
        variation = product_variations.first()
        in_cart = CartItem.objects.filter(cart__cart_no = _get_cart_id(request), variation  = variation).exists()
    except Exception as e:
        raise e

    all_color = set()
    color_size = set()
    color = None
    size = None

    if variation:
        color = variation.color
        size = variation.size

    for var in product_variations:
        all_color.add(var.color)
        if var.color == color:
            color_size.add(var.size)

    context = {
        'product' : product,
        'in_cart' : in_cart,
        'all_color': all_color,
        'color_size': color_size,
        'product_color': color,
        'product_size': size,
        'variate': variation,
    }

    return render(request, 'store/product_detail.html', context)

def variation_view(request, product_id = None, color = None, size = None):
    """"""
    try:
        product = get_object_or_404(Product,  pk = product_id)
        product_variations = Variation.objects.filter(product = product)
        color_variation = product_variations.filter(color = color)
        variation = color_variation.filter(size = size)
        if not variation.exists():
            variation = color_variation.first()
            var_id = variation.id
            size = variation.size
        else:
            size = variation[0].size
            var_id = variation[0].id
        in_cart = CartItem.objects.filter(cart__cart_no = _get_cart_id(request), variation  = var_id).exists()
    except Exception as e:
        raise e

    all_color = set()
    color_size = set()
    # color = None

    # if variation.exists():
    #     # print(variation)
    #     color = variation[0].color

    for var in product_variations:
        all_color.add(var.color)
        if var.color == color:
            color_size.add(var.size)

    context = {
        'product' : product,
        'in_cart' : in_cart,
        'all_color': all_color,
        'color_size': color_size,
        'product_color': color,
        'product_size': size,
        'variate': variation,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    """"""
    products = []
    keyword = None
    if 'keyword'in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains = keyword)| Q(product_name__icontains = keyword)).order_by('created_date')
    no_of_items = len(products)
    context = {
        'products' : products,
        "no_of_items": no_of_items,
    }
    return render(request, 'store/store.html', context)
