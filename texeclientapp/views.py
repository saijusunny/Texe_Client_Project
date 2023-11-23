from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def index(request):
    try:
        ids=request.session['userid']
        print(ids)
        usr=registration.objects.get(id=ids)
        context={
            'user':usr
        }
    except:
        context={
            'user':None
        }
    return render(request, 'index.html',context)

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
    try:
        ids=request.session['userid']
        print(ids)
        usr=registration.objects.get(id=ids)
        context={
            'user':usr
        }
    except:
        context={
            'user':None
        }
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

    return render(request, 'login.html',context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if  registration.objects.filter(email=email).exists():
            user =  registration.objects.get(email=email)

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('forget-password/reset_password_email.html',{
                'user':user,
                'domain' :current_site,
                'user_id' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 

            to_email = email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()

            messages.success(request,"Password reset email has been sent your email address.")
            return redirect('login')
        else:
            messages.error(request,"This account does not exists !")
            return redirect('forgotPassword')
    return render(request,'forget-password/forgotPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user =  registration._default_manager.get(pk=user_id)  
    except(TypeError,ValueError,OverflowError, registration.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['user_id'] = user_id 
        messages.success(request,"Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request,"The link has been expired !")
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('user_id') 
            user =  registration.objects.get(pk=uid)
            user.password = password
            user.save()
            messages.success(request,"Password reset successfull.")
            return redirect('login')

        else:
            messages.error(request,"Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'forget-password/resetPassword.html')



def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')

def product_view(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)

        context={
            'user':usr
        }
    except:
        
        context={
            'user':None
        }
    return render(request, 'user/product_view.html',context)
    
def all_item(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)

        context={
            'user':usr
        }
    except:
        
        context={
            'user':None
        }
    return render(request, 'user/all_item.html',context)

def cust(request):
    return render(request, 'user/cust.html')

def cart(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)

        context={
            'user':usr
        }
    except:
        
        context={
            'user':None
        }
    return render(request, 'user/cart.html',context)

def whistle(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)

        context={
            'user':usr
        }
    except:
        
        context={
            'user':None
        }
    return render(request, 'user/whistle.html',context)

def my_order(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)

        context={
            'user':usr
        }
    except:
        
        context={
            'user':None
        }
    return render(request, 'user/my_orders.html',context)


def profile(request):
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)

    context={
        'pro':usr
    }
    return render(request, 'user/profile.html',context)

def edit_user_profile(request,id):
    print("haii")
    if request.method == "POST":
        form = registration.objects.get(id=id)
        eml=form.email
      
        form.name = request.POST.get('name',None)

        form.dob = request.POST.get('date_of_birth',None)
        form.number = request.POST.get('phone_number',None)
        form.email = request.POST.get('email',None)
        if request.FILES.get('image',None) == None:
            pass
        else:
            form.profile = request.FILES.get('image',None)
        form.addres = request.POST.get('address',None)
        if request.POST.get('password',None) == "":
            form.password == form.password
        else:
            if request.POST.get('password',None) == request.POST.get('con_password',None):
                form.password == request.POST.get('password',None)
            else:
                messages.error(request,"Passwords do not match!")
                return redirect ("profile")
       
        form.save()
   
        
        return redirect ("profile")
    return redirect ("profile")
