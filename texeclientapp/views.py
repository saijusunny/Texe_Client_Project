from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.db.models import Q

def index(request):
    ids=request.session['userid']
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        
        email = request.POST.get('email')
        number = request.POST.get('num')
        password = request.POST.get('pass')
        cn_password = request.POST.get('cn_pass')

        if password == cn_password:

            if registration.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                if registration.objects.filter(number=number).exists():
                    messages.error(request, 'Number already exists')
                else:
                    sign = registration()
                    sign.name = request.POST.get('name')
                    sign.email = request.POST.get('email')
                    sign.number = request.POST.get('num')
                    sign.password = request.POST.get('pass')
                    sign.role = "user1"
                    sign.save()
                    return redirect('login')
        else:
          
            messages.error(request, 'Check password and confirm password')
        
        return render(request, 'signup.html') 
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('pass')

        if registration.objects.filter(Q(email=email) | Q(number=email) and Q(password=password)):
            users=registration.objects.get(Q(email=email) | Q(number=email) and Q(password=password))
            request.session['userid'] = users.id
            return redirect('index')
        else:
            messages.error(request, 'Invalid Email/Password')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')

def product_view(request):
    return render(request, 'user/product_view.html')
    
def all_item(request):
    return render(request, 'user/all_item.html')

def cust(request):
    return render(request, 'user/cust.html')

def cart(request):
    return render(request, 'user/cart.html')

def whistle(request):
    return render(request, 'user/whistle.html')



