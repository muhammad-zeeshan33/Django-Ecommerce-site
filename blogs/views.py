from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Blog
from store.models import Order, OrderItem
from .models import Comment
from products.models import Category

def blogs(request):
    categories =  Category.objects.all().filter(is_active=True)
    blogs = Blog.objects.all().filter(published=True)
     
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
        'categories': categories,
        'blogs': blogs
    }        
    return render(request,'blogs/blogs.html', context)


def blog(request, blog_id):    
    
    blogs = Blog.objects.order_by('-created').filter(published=True)[:3]
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer = customer, complete=False)
        items= order.orderitem_set.all()

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    noOfComments = Comment.objects.all().filter(blog=blog_id).count()
    
    

    categories =  Category.objects.all().filter(is_active=True)
    blog =get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.all().filter(blog = blog)
    print(comments)

    context = {
        'blog': blog,
        'categories': categories,
        'order': order,
        'blogs': blogs,
        'comments': comments,
        'noOfComments': noOfComments,
        'items': items

    }
    return render(request, 'blogs/blog.html', context)

def comment(request):
    if request.method == 'POST':
        user = request.user
        blog_id = request.POST['blog_id']
        blog = Blog.objects.get(id=blog_id)
        message =  request.POST['message']
        comment = Comment.objects.create(blog=blog, user=user, comment = message)
        comment.save()
        return redirect('/blogs/'+blog_id)
    return JsonResponse('Comment is Posted', safe=False)
