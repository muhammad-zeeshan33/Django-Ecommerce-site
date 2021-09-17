from store.views import cart
from django.db.models.fields import NullBooleanField
from django.shortcuts import get_object_or_404, render
from datetime import datetime
from products.models import Category, Product
from store.models import Order, OrderItem
from blogs.models import Blog


def index(request):    
    mens = Product.objects.order_by('-date_added').filter(category__category_name='Mens fashion')[:1]
    womens = Product.objects.order_by('-date_added').filter(category__category_name='Womens Fashion')[:1]
    footwears = Product.objects.order_by('-date_added').filter(category__category_name='Foot wears')[:1]
    sliderProducts = Product.objects.filter(category__category_name = 'Mens fashion')[:1]
    categories = Category.objects.all().filter(is_active=True)
    products = Product.objects.all().filter(is_published=True)
    blogs = Blog.objects.order_by('-created').filter(published=True)[:3]
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer = customer, complete=False)
        items= order.orderitem_set.all()
        cartItems  = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        # cartItems  = order['get_cart_items': 0,]

    context = {
        'products': products,
        'mens': mens,
        'womens': womens,
        'footwears': footwears,
        'slider': sliderProducts,
        'categories': categories,
        'oldprice': 0,        
        'items': items,
        'order': order,
        'blogs': blogs
        
    }
    return render(request, 'pages/index.html', context)


def shop(request):
    products =  Product.objects.all().filter(is_published=True)[:25]
    categories = Category.objects.all().filter(is_active=True)
    blogs = Blog.objects.order_by('-created').filter(published=True)[:3]
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer = customer, complete=False)
        items= order.orderitem_set.all()        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}        

    context= {
        'products': products,
        'categories': categories,        
        'items': items,
        'order': order,
        'blogs': blogs
    }
    return render(request , 'pages/shop.html', context)


def product(request, p_id):
    product = get_object_or_404(Product, pk=p_id)
    categories = Category.objects.all().filter(is_active=True)
    context = {
        'product': product,        
        'categories': categories
    }
    return render(request, 'pages/product.html', context)



def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    categories = Category.objects.all()
    products = Product.objects.filter(category=category)
    context = {
        'category':  category,
        'products': products,
        'categories': categories
    }
    return render(request, 'pages/category.html', context)


def search(request):
    categories = Category.objects.all()
    queryset_list=Product.objects.order_by('-date_added').filter(is_published=True)
    if 'search' in request.GET:
        search =  request.GET['search']
        if search:
            queryset_list= queryset_list.filter(name__icontains=search)
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            queryset_list= queryset_list.filter(category__category_name__iexact=category)
                        

    context = {
        'products': queryset_list,
        'categories': categories,
        'values': request.GET
    }
            
    return render(request, 'pages/search.html', context)


def contact(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'pages/contact.html', context)