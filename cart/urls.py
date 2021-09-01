from django.urls import path
from .views import cart_view, add_cart, remove_cart, remove_cart_all

urlpatterns = [
    path('', cart_view, name = 'cart'),
    path('add_cart/<int:product_pk>/color/<str:color>/size/<str:size>', add_cart, name = 'add_cart'),
    path('remove_cart/<int:product_pk>/color/<str:color>/size/<str:size>', remove_cart, name = 'remove_cart'),
    path('remove_cart_all/<int:product_pk>/color/<str:color>/size/<str:size>', remove_cart_all, name = 'remove_cart_all'),

]
