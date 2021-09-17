from os import name
from django.http.response import HttpResponse
from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from store.models import Customer


def login(request):
    if request.method ==  'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login was Successfull!')
            return redirect('index')
        else:
            messages.error(request, 'Credentials Does not match our record! Try again...')
            return redirect('login')
                    
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        get = request.POST
        fname=get['fname']
        lname=get['lname']
        username=get['username']
        email=get['email']
        password=get['password']
        password2=get['password2']   
        if len(password) >= 8:

            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'That Username is already Taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, first_name =fname, last_name=lname, password=password, email=email)
                    user.save()                    
                    CurrentUser = get_object_or_404(User, pk=user.id)
                    customer, create =Customer.objects.get_or_create(user=CurrentUser, name=fname+" "+lname, email=email)                             
                    messages.success(request, 'You are successfully registered! Login here...')
                    return redirect('login')
            else:
                messages.error(request, 'Password does not matches!')
                return redirect('register')
        else:
            messages.error(request, 'Please choose a Strong password')
            return redirect('register')    
    return render(request, 'accounts/register.html')


def logout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request, 'You are logged out Successfully!')
        return redirect('index')
    
