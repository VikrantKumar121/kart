"""kart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import store_view, product_view, search, variation_view, submit_review

urlpatterns = [
    path('', store_view, name = 'store'),
    path('category/<slug:category_slug>', store_view, name = 'search_category'),
    path('product/<int:product_id>', product_view, name = 'search_product'),
    path('product/<int:product_id>/color/<str:color>/size/<str:size>', variation_view, name = 'variation'),
    path('search/', search, name = 'search'),
    path('submit_review/<int:product_id>', submit_review, name = 'submit_review'),

]
