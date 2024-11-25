from django.shortcuts import render , redirect
from django.contrib.auth.models import auth , User
from django.contrib.auth import logout , authenticate , login
from .models import *
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.gis.geoip2 import GeoIP2
import django

from django.views.generic import ListView , DeleteView
 
# Create your views here.

print(django.get_version(),"version")



def home (request):
    products = Product.objects.all()
    categories = Category.objects.all()
    counts = Cart.objects.all().count()-1
    print(counts)
    log_user = request.user
    log_time = datetime.datetime.today()
    return render(request , "index.html" , {"products":products ,
                                             "categories":categories ,
                                             "log_user":log_user ,
                                               "log_time":log_time,
                                               "counts":counts})


def login(request):
    categories = Category.objects.all()
    if request.POST:
        email = request.POST['email']
        pwd = request.POST['password']

        username = email.lower()
        password = pwd.lower()
        user = auth.authenticate(username = username , password = password)

        login_user = User.objects.filter(username = email)
        if not(login_user):
            messages.error(request , "Invalid Username")
            return redirect('login')
        
        if user is not None:
            auth.login(request,user)
            log_user = request.user
            log_time = datetime.datetime.today()
            messages.success(request , f"Username: {log_user}<br> Time: {log_time}<br> successfully loged in")
            return redirect('home')
        else:
            messages.error(request ,"Password is incorrect")
            return redirect('login')

    return render(request , 'login.html',{"categories":categories})


def register(request):
    categories = Category.objects.all()
    if request.POST:
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        password = request.POST["password"]

        duplicate = User.objects.filter(username = email).exists()


        if duplicate:
            messages.error(request , "Username already exists")
            return redirect("register")
        
        if not(firstname and email and lastname and password):
            messages.error(request , "Please fill all the fields")
            return redirect("register")
        else:
            new_user = User.objects.create_user(first_name = firstname , last_name = lastname , username = email , password = password)
            new_user.save()
            return redirect('login')


    return render(request , 'register.html',{"categories":categories})



def logout_user(request):
    logout(request)
    return redirect('login')



def products_all(request , id):
    categories = Category.objects.all()

    products = Product.objects.get(id = id)
    # print(products.category)

    product = Product.objects.filter(category = products.category).exclude(id = id)[:4]

    return render(request , "product.html",{'products':products ,"categories":categories , 'product':product})



def cate(request , id):
    categories = Category.objects.all()
    s_category = Com.objects.filter(ct = id)
    product = Product.objects.filter(category = id)
    return render(request , "category.html" , {"categories":categories , 'product':product , "s_category":s_category})



def sub_category(request , id):
    categories = Category.objects.all()
    sub = Com.objects.get(id = id)
    print(sub , "   @   @   .   .   .   .   .   .   .   '   '   ;   ';  '   '   ;   '   ]   ]   ]   ]]  ]   ]   ]   ]   ]   ]   ]")
    # fill = Com.objects.get(ct = id)
    # print(fill,"    /   /   /   /   /   /   /   /   /   /   /   /   /   ./  .   /   /   /   /   /   /   /   /   /")
    s_category = Com.objects.filter(ct = id)
    print(s_category,"  .   .   .   /   .   /.  /   .   /   ./  .   /   .   /   .   /   .   /   .   /   ./  .   /   .   /   .   ")
    product = Product.objects.filter(brand = id)
    return render(request , "category.html" , {"categories":categories ,'product':product, "s_category":s_category})



razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
def cart(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        pro = Cart.objects.filter(user = request.user)
        print(f"Cart items for user {request.user}: {pro}")

        for item in pro:
            print(f"Product: {item.products}, Price: {item.products.price}, Quantity: {item.quantity}")


        sub_total = sum([i.products.price * i.quantity for i in pro])
        print(f'{sub_total}')
        discount_price = float(sub_total) * 0.15
        final_price = float(sub_total) - discount_price
        print(f"sub Total :-  {sub_total} - Discount {discount_price} -Final :- {final_price}")

        if sub_total > 0:
                
                currency = 'INR'
                amount = int(final_price*100)  # Rs. 200
 
                # Create a Razorpay Order
                razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                                currency=currency,
                                                                payment_capture='0'))
            
                # order id of newly created order.
                razorpay_order_id = razorpay_order['id']
                callback_url = 'paymenthandler/'
            
                # we need to pass these details to frontend.
                context = {}
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                context['razorpay_amount'] = amount
                context['currency'] = currency
                context['callback_url'] = callback_url
            
                return render(request, "cart.html",{"categories":categories ,
                                                     "pro":pro ,"sub_total":sub_total,
                                                     "discount_price":discount_price,
                                                     "final_price":final_price ,
                                                     "context" : context})

        return render(request , "cart.html",{"categories":categories ,
                                              "pro":pro ,
                                              "sub_total":sub_total,
                                              "discount_price":discount_price,
                                              "final_price":final_price})
    return redirect('login')



def add_cart(request , id):
    if request.user.is_authenticated:
        if Cart.objects.filter(products = id).exists():
            Ql = Cart.objects.get(products = id) 
            Ql.quantity +=1
            Ql.save()
            return redirect('cart')
        
        user = request.user
        new = Product.objects.get(id = id)
        pro = Cart.objects.create(products = new, user = user)
        pro.save()
        return redirect('cart')
    return redirect('login')
    

def delete_product(request , id):
     print(id)
     if Cart.objects.filter(products = id).exists():
            print("satisfiy .   .   .   .   .   .   .   .   .   ..  .   .   .   .   .   .")
            Ql = Cart.objects.get(products = id) 
            Ql.quantity -=1
            Ql.save()
            return redirect('cart')
     else:
        print("Not satisfiyng   .   ..  .   .   .   .   ..  .   .   .   .   .   .   .")
        trash = Cart.objects.get(id = id)
        trash.delete()
        return redirect('cart')
     

def about(request):
    categories = Category.objects.all()

    return render (request , "about.html",{"categories":categories})


def slider(request):
    categories = Category.objects.all()
    all =Product.objects.all() 
    return render (request , "slider.html",{"categories":categories , "all":all })


def sCate(request , brand):
    pass

@csrf_exempt
def success(request):
    messages.success(request ,f'Successfully Purchased')
    return redirect('home')