from .models import Cart, CartItem
from .views import _get_cart_id

def cart_items(request):
    """"""
    item_count = 0
    cart_items = []
    if 'admin' in request.path:
        return {}
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(cart__user = request.user)
        except:
            cart_items = []

    for item in cart_items:
        item_count += item.quantity

    context = {
        'item_count': item_count
    }

    return context
