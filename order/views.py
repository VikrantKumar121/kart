from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from store.models import Product, Variation
from .models import Order, Payment, OrderProduct
from .forms import OrderForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
import json

# Create your views here.

def payment(request):
    """"""
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user, is_ordered=False, order_no = body['orderID'])
    # print(body)

    # store transaction details in model
    payment = Payment(
        user = request.user,
        payment_no = body['transID'],
        payment_method = body['payment_method'],
        amount = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered =  True
    order.save()

    # move the cart items to order product
    cart_items = CartItem.objects.filter(cart__user = request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order = order
        orderproduct.payment = payment
        orderproduct.user = request.user
        orderproduct.product = item.product
        orderproduct.variation = item.variation
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # reduce variation quantity
        variation = item.variation
        variation.stock -= item.quantity
        variation.save()

    cart_items.delete()

    # send transaction to user

    mail_subject = 'Thank you for shopping'
    msg = render_to_string('order/order_recieved.html', {
        'user': request.user,
        'order_id': order.order_no,
        'trans_id': payment.payment_no,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, msg, to=[to_email])
    send_email.send()

    data = {
        'order_no': order.order_no,
        'transID': payment.payment_no,
    }
    return JsonResponse(data)

    # return render(request, 'order/payment.html')

def place_order(request):
    """"""
    cur_user = request.user

    cart_items = CartItem.objects.filter(cart__user = cur_user)
    item_count = cart_items.count()

    if item_count <=0:
        return redirect('store')

    quantity = 0
    total = 0
    tax = 0
    grand_total = 0

    for item in cart_items:
        quantity += item.quantity
        total += item.product.price*item.quantity

    tax = (5*total)/100
    grand_total = total + tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = cur_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone_no = form.cleaned_data['phone_no']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate orde no
            today = datetime.date.today()
            year = int(today.strftime('%Y'))
            month = int(today.strftime('%m'))
            day = int(today.strftime('%d'))
            date = datetime.date(year,month,day)
            cur_date = date.strftime("%Y%m%d")
            order_no = cur_date+ str(data.id)
            data.order_no = order_no
            data.save()

            order = Order.objects.get(user=cur_user, is_ordered = False, order_no = order_no)

            context = {
                'order': order,
                'cart_items': cart_items,
                'quantity':quantity,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }

            return render(request, 'order/payment.html', context)

    return redirect('checkout')

def order_complete(request):
    """"""
    order_no = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')
    # print(order_no, payment_id)

    try:

        order = Order.objects.get(order_no = order_no, is_ordered = True)
        product = OrderProduct.objects.filter(order = order)
        payment = Payment.objects.get(payment_no = payment_id)

        sub_total = order.order_total - order.tax

        context = {
            'order': order,
            'products': product,
            'payment': payment,
            'subtotal': sub_total,
            'order_total': order.order_total,
            'tax': order.tax
        }

        return render(request, 'order/order_complete.html', context)

    except (Order.DoesNotExist, Payment.DoesNotExist):
        return render(request, 'order/order_complete.html')
        # return redirect('home')
