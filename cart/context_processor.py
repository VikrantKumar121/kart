from .models import Cart, CartItem
from .views import _get_cart_id

def cart_items(request):
    """"""
    item_count = 0
    if 'admin' in request.path:
        return {}
    try:
        cart_items = CartItem.objects.filter(cart__cart_no = _get_cart_id(request))
        for item in cart_items:
            item_count += item.quantity

    except CartItem.DoesNotExist:
        item_count = 0

    context = {
        'item_count': item_count
    }
    
    return context
