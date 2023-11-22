from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

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



