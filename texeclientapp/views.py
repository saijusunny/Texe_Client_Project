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
from django.contrib.auth import authenticate
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
        user = authenticate(username=email, password=password)

        if registration.objects.filter(Q(email=email) | Q(number=email) and Q(password=password)):
            users=registration.objects.get(Q(email=email) | Q(number=email) and Q(password=password))
            request.session['userid'] = users.id
            return redirect('index')
        elif user.is_superuser:
                    request.session['userid'] = request.user.id
                    return redirect('admin_home')
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


#-----------------------------------------------admin

def admin_home(request):
    return render(request, "admin/admin_home.html")

def create_banner(request):
    banners = banner.objects.all().last
    
    context={
        "banners":banners,
    }
    
    return render(request,"admin/create_banner.html",context)
def save_banner(request):
    if request.method=="POST":
        ban=banner()
        ban.top_banner = request.FILES.get("main_banner", None)
        ban.top_link = request.POST.get("main_banner_link", None)
        ban.middle_banner =  request.FILES.get("middile_banner", None)
        ban.middle_link = request.POST.get("middle_banner_link", None)
        ban.bottom_banner1 =  request.FILES.get("last_banner1", None)
        ban.bottom_link1 = request.POST.get("bottom_banner_link1", None)
        ban.bottom_banner2 =  request.FILES.get("last_banner2", None)
        ban.bottom_link2 = request.POST.get("bottom_banner_link2", None)
        ban.save()
        return redirect("admin_home")
    return redirect("create_banner")

def edit_banner(request,id):
    if request.method=="POST":
        ban=banner.objects.get(id=id)
        ban.top_banner = request.FILES.get("main_banner", None)
        ban.top_link = request.POST.get("main_banner_link", None)
        ban.middle_banner =  request.FILES.get("middile_banner", None)
        ban.middle_link = request.POST.get("middle_banner_link", None)
        ban.bottom_banner1 =  request.FILES.get("last_banner1", None)
        ban.bottom_link1 = request.POST.get("bottom_banner_link1", None)
        ban.bottom_banner2 =  request.FILES.get("last_banner2", None)
        ban.bottom_link2 = request.POST.get("bottom_banner_link2", None)
        ban.save()
        return redirect("admin_home")
    return redirect("create_banner")


def admin_category(request):
    cat_all=category.objects.all()
    return render(request,'admin/create_category.html',{'cat_all':cat_all})

def admin_save_category(request):
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name', None)

        categorys = category(
            category_name = category_name,
        )
        categorys.save()

        
        return redirect('admin_category')

    return redirect('admin_category')

def admin_subcategory(request):
    
    if request.method == 'POST':
        category_id = request.POST.get('category_name', None)
        cat=category.objects.get(id=category_id)
        subcat = request.POST.getlist('subcat[]')
        print(subcat)
        if subcat:
            mappeds = zip(subcat)
            mappeds=list(mappeds)
            for ele in mappeds:
            
                created = sub_category.objects.get_or_create(subcategory=ele[0], category=cat)
        else: 
            pass


        return redirect('admin_home')

    return redirect('admin_category')

def edit_category(request,id):
    if request.method == 'POST':
        cat=category.objects.get(id=id)
        
        cat.category_name = request.POST.get('category_name',None)
       
       
        cat.save()
        return redirect('ad_category_list')

    return redirect('ad_category_list')

def edit_subcategory(request,id):
    
    if request.method == 'POST':
        category_id = request.POST.get('category_name', None)
        cat=category.objects.get(id=id)
        subcat = request.POST.getlist('subcat[]')
        dels=sub_category.objects.filter(category=id).delete()

        if subcat:
            mappeds = zip(subcat)
            mappeds=list(mappeds)
            for ele in mappeds:
            
                created = sub_category.objects.get_or_create(subcategory=ele[0], category=cat)
        else: 
            pass


        return redirect('ad_category_list')

    return redirect('ad_category_list')

def ad_category_list(request):
    cat=category.objects.all()
    cat_sub = sub_category.objects.all()
    return render(request, 'admin/ad_category_list.html', {'cat': cat,'cat_sub':cat_sub})

def delete_cat(request,id):
    cat=category.objects.get(id=id)
    cat.delete()
    cat_sub = sub_category.objects.filter(category=id).delete()
    return redirect('ad_category_list')

def ex_all_events(request):
    all_events = Events.objects.all()
    out=[]
    for event in all_events:
        out.append({
            "title":event.name,
            "id":event.id,
            "start":event.start.strftime("%m/%d/%Y, %H:%M:%S"), 
        })
    return JsonResponse(out, safe=False)
 
def product(request):
    return render(request, 'admin/product.html')

def admin_add_item(request):

    item_categories = category.objects.all()
    cat = sub_category.objects.all()
    
    if request.method == 'POST':
        form_data = request.POST.dict()

        title = form_data.get('title', None)
        price = form_data.get('price', None)

        
        offer_percentage = form_data.get('offer_percentage', None)
        offer_prices = form_data.get('offer_price', None)
        image = request.FILES.get('image', None)
        category_id = form_data.get('categories', None)
        under_category = form_data.get('under_category', None)
        title_description = form_data.get('title_description', None)
        description = form_data.get('description', None)
        sub_categoryies = form_data.get('subcategories', None)
       
        categorys = get_object_or_404(category, pk=category_id)
        

        new_item = item(
            category = categorys,
            name = title,
            price = price,
            buying_count = 0,
            offer = offer_percentage,
            offer_price=offer_prices,
            image = image,
            sub_category=sub_categoryies,
            under_category = under_category,
            title_description = title_description,
            description = description
        )
        new_item.save()
        return redirect('product')
    context={
        'item_categories':item_categories,

        'sub_categories':cat,
    }

    return render(request,'admin/create_product.html',context)




def create_product(request):
    
    return render(request, 'admin/create_product.html')

def ex_add_event(request):
    pass
 
def ex_update(request):
    pass
 
def ex_remove(request):
   pass