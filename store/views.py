from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from products.models import Product
from .models import Order, OrderItem, ShippingAddress
from products.models import Category
from django.http import JsonResponse
from .choices import state_choices
from datetime import datetime
from django.views import View
from django.conf import settings
import json
import stripe


def cart(request):
    categories = Category.objects.all().filter(is_active=True)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer = customer, complete=False)
        items= order.orderitem_set.all()

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'items': items,
        'order': order,
        'categories': categories
    }    
    return render(request, 'store/cart.html', context)

def updateItem(request):                
    if request.method == 'GET':        
        productId = request.GET['productId']
        action =request.GET['action']
        customer = request.user.customer        
        product = Product.objects.get(id=productId)    
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)
        
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
            return redirect('index')

        if action == 'delete':
            orderItem.delete()            
            return redirect('cart')

    else:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, create = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        if action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()
    
    
        if orderItem.quantity <= 0:
            orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)


def checkout(request):
    categories = Category.objects.all().filter(is_active=True)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer = customer, complete=False)
        items= order.orderitem_set.all()

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'items': items,
        'order': order,
        'state_choices': state_choices,
        'categories': categories
    }    
    return render(request, 'store/checkout.html', context)

def processOrder(request):
    data = json.loads(request.body)
    transaction_id=datetime.now().timestamp()
    print('data:', request.body )
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)        
        order.transaction_id=transaction_id                
        order.save()
        ShippingAddress.objects.create(
            customer=customer,
            order = order,
            address = data['address'],
            city = data['city'],
            state = data['state'],
            zipcode = data['zipcode']
        )
    return JsonResponse('Payment Completed', safe=False)

# ======================================= payment integeration scripts ==========================================

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateCheckoutSessionView(View):
    
    def post(self ,*args, **kwargs):    
        customer = self.request.user.customer
        order , create = Order.objects.get_or_create(customer=customer, complete=False)    
        cart_total = order.get_cart_total * 100        
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': cart_total,
                        'product_data':{
                            'name': order.customer.name
                        } 
                    },
                'quantity': 1

                },
            ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + reverse('paymentSuccess'),
            cancel_url=YOUR_DOMAIN + reverse('paymentError'),
        )
        return redirect(checkout_session.url, code=303)

        
def paymentSuccess(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)        
        order.complete=True                
        order.save()
    context = {
        'payment_status': 'success'
    }
    return render(request, 'store/confirmation.html', context)

def paymentErr(request):
    context = {
        'payment_status': 'error'
    }
    return render(request, 'store/confirmation.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout-session-completed':
        session = event['data']['object']

        if session.payment_status == 'paid':
            line_item = session.line_items(session.id, limit=1).data[0]
            order_id=line_item['description']
            fulfill_order(order_id)

    # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(order_id):
    order = Order.objects.get(id=order_id)
    order.complete = True
    order.date_orderd= datetime.now()
    order.save()    