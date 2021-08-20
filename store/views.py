from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
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
        products = Product.objects.filter(is_avail = True, category = search_category)

    else:
        products = Product.objects.filter(is_avail = True)

    no_of_items = len(products)

    context = {
        'categories': categories,
        'products' : products,
        "no_of_items": no_of_items,
    }

    return render(request, 'store/store.html', context)

def product_view(request, category_slug = None, product_id = None):
    """"""
    try:
        product = Product.objects.get(category__slug = category_slug, pk = product_id)
    except Exception as e:
        raise e
    context = {
        'product' : product,
    }

    return render(request, 'store/product_detail.html', context)
