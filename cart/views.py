from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from store.models import Product

# Create your views here.

def cart_view(request, cart_pk = None):
    """"""
    cart = None
    cart_item = []
    if cart_pk != None:
        cart = get_object_or_404(Cart, pk = cart_pk)
        cart_items = [get_object_or_404(CartItem, item) for item in cart.items]

    context = {
        'cart' : cart,
        'cart_items': cart_items
    }

    return render(request,'store/cart.html')
