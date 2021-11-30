
from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime

from .models import * 
from .utils import cartData, guestOrder


def index(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    categories = Category.objects.all()
    reviews = Review.objects.all()
    blogs = Blog.objects.all()

    context = {'products': products,
               'categories': categories,
               'reviews': reviews,
               'blogs': blogs,
               'cartItems': cartItems,
               'items': items,
               'order': order}

    return render(request, 'main/index.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0 or action == 'delete':
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            phone = data['shipping']['phone'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete...', safe=False)
