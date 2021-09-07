from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required

# Create your views here.

def _get_cart_id(request):
    """"""
    id = request.session.session_key
    if not id:
        id = request.session.create()
    return id

@login_required(login_url = 'login')
def add_cart(request, product_pk = None, color = None, size = None):
    """"""
    product = get_object_or_404(Product, id = product_pk)
    variation = get_object_or_404(Variation, product = product, color = color, size = size)
    cur_cart = None
    cart_item = None

    try:
        cur_cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist :
        cur_cart =  Cart.objects.create(
            user = request.user
        )
        cur_cart.save()

    try:
        cart_item = CartItem.objects.get(cart = cur_cart, product = product, variation = variation)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist :
        cart_item = CartItem.objects.create(
            product = product,
            cart = cur_cart,
            variation = variation,
        )
        cart_item.save()

    return redirect('cart')

@login_required(login_url = 'login')
def remove_cart(request, product_pk = None, color = None, size = None):
    """"""
    product = get_object_or_404(Product, id = product_pk)
    variation = get_object_or_404(Variation, product = product, color = color, size = size)
    cart = Cart.objects.get(user = request.user)
    cart_item = None
    try:
        cart_item = CartItem.objects.get(cart = cart, product = product, variation = variation)
        cart_item.quantity -= 1
        cart_item.save()
        if cart_item.quantity < 1 :
            cart_item.delete()
    except Cart.DoesNotExist :
        return redirect('cart')

    return redirect('cart')

@login_required(login_url = 'login')
def remove_cart_all(request, product_pk = None, color = None, size = None):
    """"""
    product = get_object_or_404(Product, id = product_pk)
    variation = get_object_or_404(Variation, product = product, color = color, size = size)
    cart = Cart.objects.get(user = request.user)
    cart_item = None
    try:
        cart_item = CartItem.objects.get(cart = cart, product = product, variation = variation)
        cart_item.quantity = 0
        cart_item.delete()
    except Cart.DoesNotExist :
        return redirect('cart')

    return redirect('cart')

@login_required(login_url = 'login')
def cart_view(request):
    """"""

    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user = request.user)

    cart_items = CartItem.objects.filter(cart = cart, is_active = True )

    quantity = 0
    total = 0
    tax = 0
    grand_total = 0

    for item in cart_items:
        quantity += item.quantity
        total += item.product.price*item.quantity

    tax = (5*total)/100
    grand_total = total + tax

    context = {
        'cart' : cart,
        'quantity': quantity,
        'total': total,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request,'store/cart.html',context)

@login_required(login_url = 'login')
def checkout(request):
    """"""
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user = request.user)
    cart_items = CartItem.objects.filter(cart = cart, is_active = True )
    quantity = 0
    total = 0
    tax = 0
    grand_total = 0

    for item in cart_items:
        quantity += item.quantity
        total += item.product.price*item.quantity

    tax = (5*total)/100
    grand_total = total + tax

    context = {
        'cart' : cart,
        'quantity': quantity,
        'total': total,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)
