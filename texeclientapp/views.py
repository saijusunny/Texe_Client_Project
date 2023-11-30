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
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize

def index(request):
    cat_id=category.objects.all().first()
    items=item.objects.all()
    cat=category.objects.all()
    sub=sub_category.objects.all()
    trend=item.objects.all().order_by('-buying_count')[:10]
    bann=banner.objects.all().last()
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)
        wish=wishlist.objects.filter(user=usr)
        
        context={
            'user':usr,
            "items":items,
            "wish":wish,
            'bann':bann,
            'cat':cat,
            'sub':sub,
            'trend':trend,
        }
    except:
        context={
            'user':None,
            "items":items,
            'cat':cat,
            'sub':sub,
            'bann':bann,
            'trend':trend,
            
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
                    sign.addres = request.POST.get('address')
                    sign.dob = request.POST.get('dob')
                    sign.location = request.POST.get('location')
                    sign.pin = request.POST.get('pin')
                    sign.country = request.POST.get('country')      
                    sign.state = request.POST.get('state')
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

def product_view(request,id):
    items=item.objects.get(id=id)
    sub=sub_images.objects.filter(item=items)
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)

        context={
            'user':usr,
            'items':items,
            'sub':sub,
        }
    except:
        
        context={
            'user':None,
            'items':items,
            'sub':sub,
        }
    return render(request, 'user/product_view.html',context)
    
def all_item(request):

    itm = item.objects.all()
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)
        wish=wishlist.objects.filter(user=usr)

        context={
            'user':usr,
            "itm":itm,
            "wish":wish,

        }
    except:
        context={
            'user':None,
            "itm":itm,
            
        }
        
    
    return render(request, 'user/all_item.html', context)
  

def cust(request):
    return render(request, 'user/cust.html')

def carts(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)
        crt= cart.objects.filter(user=usr, status="cart")
    
        context={
            'user':usr,
            'crt':crt,
        }
    except:
        if request.session.has_key('userid'):
            pass
        else:
            return redirect('/')
        context={
            'user':None
        }
    return render(request, 'user/cart.html',context)



def save_cart(request,id):
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
    
    itm=item.objects.get(id=id)
    if request.method=="POST":
        if request.POST.get('cart_id',None) == "":
            carts=cart()
            
            carts.user = usr
            carts.item = itm
            carts.size= "XS"
            carts.color= "white"
            carts.meterial= "Cotton"
            carts.status="cart"
            carts.design= request.FILES.get('design',None)
            carts.logo= request.FILES.get('logo',None)
            carts.name= request.POST.get('text',None)
            carts.number= request.POST.get('number',None)
            mdl_id=request.POST.get('model_num1', None)
            mdl=sub_images.objects.get(id=mdl_id)
            carts.model = mdl
            carts.save()
            return redirect('index')
        else:
            
            cart_id=request.POST.get('cart_id',None)
            crt=cart.objects.get(id=cart_id)
            if crt.size==None:
                crt.size= "XS"
            else:
                pass
            if crt.color==None:
                crt.color= "white"
            else:
                pass

            if crt.meterial==None:
                crt.meterial= "Cotton"
            else:
                pass
            if crt.model==None:
                mdl_id=request.POST.get('model_num1', None)
                mdl=sub_images.objects.get(id=mdl_id)
                crt.model = mdl
            else:
                pass
            
            crt.design= request.FILES.get('design',None)
            crt.logo= request.FILES.get('logo',None)
            crt.name= request.POST.get('text',None)
            crt.number= request.POST.get('number',None)
            crt.status="cart"
            crt.save()
            return redirect('index')


    return redirect('carts')



def cart_cust_size(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
    if cart_id=="":
        crt=cart()
        crt.user = usr
        crt.item = itm
        crt.model = None
    else:
        crt=cart.objects.get(id=cart_id)

    
    crt.size= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def cart_change_color(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
    if cart_id=="":
        crt=cart()
        crt.user = usr
        crt.item = itm
        crt.model = None
    else:
        crt=cart.objects.get(id=cart_id) 

    
    crt.color= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def cart_change_meterial(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
    if cart_id=="":
        crt=cart()
        crt.user = usr
        crt.item = itm
        crt.model = None
    else:
        crt=cart.objects.get(id=cart_id) 

    
    crt.meterial= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})


def cart_change_model(request):
    ele = request.GET.get('ele')
    model=sub_images.objects.get(id=ele)
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
    if cart_id=="":
        crt=cart()
        crt.user = usr
        crt.item = itm
        crt.model = model
    else:
        crt=cart.objects.get(id=cart_id) 

    
    crt.model = model
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def checkout(request):
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)

    if request.method =="POST":
        total_amount = request.POST.get('sum')

        chk=orders()
        chk.user = usr
        chk.total_amount=total_amount
        chk.date=datetime.now()
        chk.status="checkout"
        chk.save()
        item_id =request.POST.getlist('item_id[]') 
        qty =request.POST.getlist('qty[]') 
        cart_id=request.POST.getlist('cart_id[]') 

        if len(item_id)==len(qty)==len(cart_id):
            mapped2 = zip(item_id,qty,cart_id)
            mapped2=list(mapped2)
         
            for ele in mapped2:
                itm=item.objects.get(id=ele[0])
                itm.buying_count=int(itm.buying_count+1)
                itm.save()
              
                sub=sub_category.objects.get(id=itm.sub_category.id)
                print("sub.buying_count")
                print(sub.buying_count)
                sub.buying_count=int(sub.buying_count)+1
                sub.save()

                crts= cart.objects.get(id=ele[2])
                crts.status="checkout"
                crts.save()
                tot=float(itm.offer_price)*int(ele[1])
                created = checkout_item.objects.create(item=itm,qty=ele[1],item_name=itm.name,item_price=tot, orders=chk, cart=crts)

        chk_item=checkout_item.objects.filter(orders=chk)
      
        # lst=""
        # for i in chk_item:
        #     rcp="\n\nItem : "+str(i.item_name)+'\nAmount : '+str(i.item_price)+' * '+str(i.qty)+' = '+str(i.item_price)
        #     lst+=rcp
     
        # tot="\n\nTotal Amount : "+str(total_amount)
        
        # message = 'Greetings from Malieakal\n\nReciept,\n\nName :'+str(usr.name)+str(usr.lastname)+'\nAddress :'+str(pro.address)+'\n\n'+str(lst)+str(tot)

        # pywhatkit.sendwhatmsg_instantly(
        #     phone_no="+918848937577", 
        #     message=""+str(message),
        # )
          
    
        return redirect("my_order")
    return redirect("my_order")

def whistle(request):
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)
        wish=wishlist.objects.filter(user=usr)

        context={
            'user':usr,
            'wish':wish,
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
        ords=orders.objects.filter(user=usr, status="checkout")
        ords_itm=checkout_item.objects.all()
        context={
            'user':usr,
            'ords':ords,
            'ords_itm':ords_itm,
        }
    except:
        
        context={
            'user':None
        }
    return render(request, 'user/my_orders.html',context)

def cancel_order(request,id):
    ords=orders.objects.get(id=id)
    ords.status=="cancel"
    ords.save()
    return redirect('my_order')

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
        form.location = request.POST.get('location')
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

def add_wishlist(request):
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
    ele = request.GET.get('ele')
    itm=item.objects.get(id=ele)
    wis=wishlist()
    wis.user=usr
    wis.item=itm
    wis.save()

    return JsonResponse({"status":" not"})

def remove_wishlist(request):
    ele = request.GET.get('ele')
    ids=request.session['userid']
    usr=registration.objects.get(id=ids)
  
    wis=wishlist.objects.get(id=ele).delete()
  
    return JsonResponse({"status":" not"})


def search(request):

    
    if request.method=="POST":
        search=request.POST.get("search",None)
        itm = item.objects.filter(models.Q(name__icontains=search) |models.Q(title_description__icontains=search))
        try:
            ids=request.session['userid']
            usr=registration.objects.get(id=ids)
            wish=wishlist.objects.filter(user=usr)

            context={
                'user':usr,
                "itm":itm,
                "wish":wish,
    
            }
        except:
            context={
                'user':None,
                "itm":itm,
                
            }
            
        
        return render(request, 'user/all_item.html', context)
    return redirect('index')

def get_items(request):
    ele = request.GET.get('ele')
    
    # Perform a database query to fetch items based on the selected category
    items = item.objects.filter(category=ele)
    
    # Convert QuerySet to list for JsonResponse
    items_list = list(items)
    print(items_list)

    items_json = serialize('json', items_list)
    return JsonResponse({"status":" not","items_list": items_json}, safe=False)

def show_category(request, id):
    

    cat=sub_category.objects.get(id=id)
    itm = item.objects.filter(sub_category=cat)
    try:
        ids=request.session['userid']
        usr=registration.objects.get(id=ids)
        wish=wishlist.objects.filter(user=usr)

        context={
            'user':usr,
            "itm":itm,
            "wish":wish,

        }
    except:
        context={
            'user':None,
            "itm":itm,
            
        }

    return render(request, 'user/all_item.html', context)

def delete_cart(request, id):
    car=cart.objects.get(id=id)
    car.delete()
    return redirect('carts')
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
        ban.top_banner1 = request.FILES.get("main_banner1", None)
        ban.top_link1 = request.POST.get("main_banner_link1", None)

        ban.top_banner2 = request.FILES.get("main_banner2", None)
        ban.top_link2 = request.POST.get("main_banner_link2", None)

        ban.top_banner3 = request.FILES.get("main_banner3", None)
        ban.top_link3 = request.POST.get("main_banner_link3", None)

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
        if request.POST.get("main_banner1", None)=="":
     
            pass
        else:
          
            ban.top_banner1 = request.FILES.get("main_banner1", None)
            
        ban.top_link1 = request.POST.get("main_banner_link1", None)

        if request.POST.get("main_banner2", None)=="":
            pass
        else:
            ban.top_banner2 = request.FILES.get("main_banner2", None)
            
        ban.top_link2 = request.POST.get("main_banner_link2", None)

        if request.POST.get("main_banner3", None)=="":
            pass
        else:
            ban.top_banner3 = request.FILES.get("main_banner3", None)
        ban.top_link3 = request.POST.get("main_banner_link3", None)

        if request.POST.get("middile_banner", None)=="":
            pass
        else:
            ban.middle_banner =  request.FILES.get("middile_banner", None)

        
        ban.middle_link = request.POST.get("middle_banner_link", None)

        if request.POST.get("last_banner1", None)=="":
            pass
        else:
            ban.bottom_banner1 =  request.FILES.get("last_banner1", None)
        
        ban.bottom_link1 = request.POST.get("bottom_banner_link1", None)
        if request.POST.get("last_banner2", None)=="":
            pass
        else:
            ban.bottom_banner2 =  request.FILES.get("last_banner2", None)
        
        ban.bottom_link2 = request.POST.get("bottom_banner_link2", None)
        ban.save()
        return redirect("admin_home")
    return redirect("create_banner")


def admin_category(request):
    cat_all=category.objects.all()
    return render(request,'admin/create_category.html',{'cat_all':cat_all})

def admin_ad_category(request):
    return render(request, 'admin/ad_main_cat.html')

def admin_save_category(request):
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name', None)

        categorys = category(
            category_name = category_name,
        )
        categorys.save()

        
        return redirect('ad_category_list')

    return redirect('ad_category_list')

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

    return redirect('ad_category_list')

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
    items=item.objects.all()

    return render(request, 'admin/product.html',{'items':items})

def admin_add_item(request):

    item_categories = category.objects.all()
    cat = sub_category.objects.all()
    
    if request.method == "POST":
        form_data = request.POST.dict()

        title = form_data.get('title', None)
        price = form_data.get('price', None)

        
        offer_percentage = form_data.get('offer_percentage', None)
        offer_prices = form_data.get('offer_price', None)
        image = request.FILES.get('image', None)
        category_id = form_data.get('categories', None)
        title_description = form_data.get('title_description', None)
        sb_cat = form_data.get('subcategories', None)
        sub_categoryies = sub_category.objects.get(subcategory=sb_cat)
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
            title_description = title_description,
            subcategory=sb_cat,
        )
        new_item.save()
        subimg = request.FILES.getlist('sub_img[]')


        if subimg:
            mappeds = zip(subimg)
            mappeds=list(mappeds)
            for ele in mappeds:
            
                created = sub_images.objects.get_or_create(image=ele[0], item=new_item)
        else: 
            pass


        return redirect('product')
    context={
        'item_categories':item_categories,
        
        'sub_categories':cat,
    }

    return render(request,'admin/create_product.html',context)

def edit_item(request,id):
    item_categories = category.objects.all()
    cat = sub_category.objects.all()
    items=item.objects.get(id=id)

    sub_img=sub_images.objects.filter(item_id=items.id)
    
    if request.method == "POST":
        form_data = request.POST.dict()

        title = form_data.get('title', None)
        price = form_data.get('price', None)

        
        offer_percentage = form_data.get('offer_percentage', None)
        offer_prices = form_data.get('offer_price', None)
        image = request.FILES.get('image', None)
        cat = form_data.get('categories', None)
        title_description = form_data.get('title_description', None)
        sb_cat = form_data.get('subcategories', None)
        sub_categoryies = sub_category.objects.get(subcategory=sb_cat)
    
  
        categorys = category.objects.get(id=cat)

        items.category = categorys
        items.name = title
        items.price = price
        items.buying_count = 0
        items.offer = offer_percentage
        items.offer_price=offer_prices
        if image==None:
            pass
        else:

            items.image = image
        items.sub_category=sub_categoryies
        items.title_description = title_description
        items.subcategory=sb_cat
      
        items.save()
        subimg = request.FILES.getlist('sub_img[]')


        if subimg:

            sub_images.objects.filter(item=items).delete()
            mappeds = zip(subimg)
            mappeds=list(mappeds)
            for ele in mappeds:
            
                created = sub_images.objects.get_or_create(image=ele[0], item=items)
        else: 
            pass


        return redirect('product')
    context={
        'item_categories':item_categories,
        'items':items,
        'sub_categories':cat,
        'sub_img':sub_img,
    }

    return render(request,'admin/edit_item.html',context)


def order(request):
    orde = orders.objects.filter(status="checkout").order_by("-id")
    ord_item=checkout_item.objects.all()
    context={
        "orders":orde,
        "ord_item":ord_item,
    }
    return render(request,'admin/orders.html', context)

def change_order_status(request):
    ele = request.GET.get('ele')
    count = request.GET.get('count')
    itm=orders.objects.get(id=ele)

    itm.stage_count=count
    if int(count)==6:
        itm.status='arrived'
    else:
        itm.status='delivery'
    itm.save()
    return JsonResponse({"status":" not"})

def order_details(request,id):
    orde = orders.objects.filter(status="delivery", id=id).order_by("-id")
    ord_item=checkout_item.objects.filter(orders_id=id)
    context={
        "orders":orde,
        "ord_item":ord_item,
    }
    return render(request, 'admin/order_details.html', context)

def delivery_orders(request):
    orde = orders.objects.filter(status="delivery").order_by("-id")
    ord_item=checkout_item.objects.all()
    context={
        "orders":orde,
        "ord_item":ord_item,
    }
    return render(request,'admin/delivery_orders.html', context)

def delivery_order_details(request,id):
    orde = orders.objects.filter(status="delivery", id=id).order_by("-id")
    ord_item=checkout_item.objects.filter(orders_id=id)
    context={
        "orders":orde,
        "ord_item":ord_item,
    }
    return render(request, 'admin/delivery_order_details.html', context)


def ex_add_event(request):
    pass
 
def ex_update(request):
    pass
 
def ex_remove(request):
   pass

def remove_sub_cat(request):
    cat_id = request.GET.get('cat_id')
    cat=sub_category.objects.get(id=cat_id).delete()
    return JsonResponse({"status":" not"})

def user_list_view(request):
    staff_members = registration.objects.filter(role='user1')
    return render(request, 'admin/users_list.html', {'staff_members': staff_members})

def delete_user(request,id):
    form = registration.objects.get(id=id)

    form.delete()

    return redirect ("user_list_view")

def export_user_excel(request):
    st_dt=request.POST.get('str_dt')
    en_dt=request.POST.get('end_dt')
    prop=registration.objects.filter(joindate__gte=st_dt,joindate__lte=en_dt)
    # Create an Excel workbook and get the active sheet
    workbook = Workbook()
    sheet = workbook.active

    # Add column headers to the Excel sheet
    headers = ['Reg No.',"Join Date","Name","Email id","ph_no","Address", "Gender", "D.O.B"]  # "Replace with your actual column names
    sheet.append(headers)

    # Add data rows to the Excel sheet
    count = 1
    for item in prop:
        
        row = [item.id,item.joindate,item.name,item.email,item.number,item.address,item.gender,item.date_of_birth] # Replace with your actual column names
        sheet.append(row)
        count+=1

    # Set the response headers for the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=filtered_data.xlsx'

    # Save the Excel workbook to the response
    workbook.save(response)

    return response
