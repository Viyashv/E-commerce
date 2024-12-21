from django.http import JsonResponse
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
from django.db.models import Q
from django.utils.safestring import mark_safe

 
# Create your views here.

print(django.get_version(),"version")

class HomePageView: # Logic for Home Page/search/sorting

    def home (request): # Home page
        products = Product.objects.all()
        categories = Category.objects.all()
        counts = max(0,Cart.objects.all().count()-1)
        return render(request , "index.html" , {"products":products ,"categories":categories ,"counts":counts})

    # Fuction to sort the home page Products
    def sort_products(request):
        counts = Cart.objects.all().count()-1
        categories = Category.objects.all()
        sort_option = request.GET.get('sort' , "a-Z")
        if sort_option == 'a-z':
            products = Product.objects.order_by('name')
        elif sort_option == 'z-a':
            products = Product.objects.order_by('-name')
        elif sort_option == 'low-to-high':
            products = Product.objects.order_by('price')
        elif sort_option == 'high-to-low':
            products = Product.objects.order_by('-price')
        return render(request , "index.html" , {"products":products ,"categories":categories ,"counts":counts})
        
    # Fuction to handle search bar logic
    def search_view(request):
        query = request.GET.get('search')  # Get the search query from the GET request
        results = Product.objects.none()  # Default to no results
        categories = Category.objects.all()
        counts = max(0,Cart.objects.all().count()-1)
        if query:
            results = Product.objects.filter(Q(name__icontains=query)|Q(brand__brand__icontains=query))  # Filter products based on the search query
        return render(request, 'search_results.html', {'results': results, 'query': query ,"counts":counts ,"categories":categories})


def login(request): # Login page
    categories = Category.objects.all()
    counts = max(0,Cart.objects.all().count()-1)
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username = username , password = password)

        login_user = User.objects.filter(username = username)
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

    return render(request , 'login.html',{"categories":categories,"counts":counts})


def register(request): # Register Page
    categories = Category.objects.all()
    counts = max(0, Cart.objects.count() - 1)
    if request.POST:
        # Retrieve form data
        firstname = request.POST.get("firstname", "").strip()
        lastname = request.POST.get("lastname", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        print(f"firstname :- {firstname} - lastname :- {lastname} - email :- {email} - username :- {username} - password :- {password}")

         # Check for duplicate username or email
        if User.objects.filter(Q(username__iexact=username) | Q(email__iexact=email)).exists():
            messages.error(request , "Username or email already exists")
            return redirect("register")
        
        if not(firstname and email and lastname and password):
            messages.error(request , "Please fill all the fields")
            return redirect("register")
        else:
            new_user = User.objects.create_user(first_name = firstname ,last_name = lastname ,username = username ,password = password ,email=email)
            new_user.save()
            return redirect('login')
    return render(request , 'register.html',{"categories":categories,"counts":counts})


razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
class CartPageViews:
    #cart function to display the cart items and handle the payment
    def cart(request):
        if request.user.is_authenticated:
            counts = Cart.objects.all().count()-1

            ord_counts = Cart.objects.filter(ord_status = True).count()
            cart_counts = Cart.objects.filter(ord_status = False).count()-1

            categories = Category.objects.all()

            para = request.GET.get('status', 'False')  # Default is 'False'
            status = para.lower() == 'true'  # Converts to True if 'status' is 'True' (case-insensitive), else False

            pro = Cart.objects.filter(user = request.user)

            sub_total = sum([i.products.price * i.quantity for i in pro if i.ord_status == False])
            discount_price = float(sub_total) * 0.15
            final_price = float(sub_total) - discount_price

            # Get IDs of items with ord_status == False
            pending_ids = [str(i.id) for i in pro if i.ord_status == False]

            if sub_total > 0:
                    
                    currency = 'INR'
                    amount = int(final_price*100)  # Rs. 200
    
                    # Create a Razorpay Order
                    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                                    currency=currency,
                                                                    payment_capture='0'))
                
                    # order id of newly created order.
                    razorpay_order_id = razorpay_order['id']

                    # Pass IDs in callback_url as query parameters
                    pending_ids_param = ",".join(pending_ids)  # Create a comma-separated list of IDs
                    callback_url = f'paymenthandler/?pending_ids={pending_ids_param}'
                
                    # we need to pass these details to frontend.
                    context = {}
                    context['razorpay_order_id'] = razorpay_order_id
                    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                    context['razorpay_amount'] = amount
                    context['currency'] = currency
                    context['callback_url'] = callback_url
                
                    return render(request, "cart.html",{"categories":categories ,
                                                        "pro":pro ,
                                                        "sub_total":sub_total,
                                                        "discount_price":discount_price,
                                                        "final_price":final_price ,
                                                        "context" : context,
                                                        "counts":counts ,
                                                        'status': status,
                                                        "ord_counts":ord_counts,
                                                        "cart_counts":cart_counts,
                                                        })

            return render(request , "cart.html",{"categories":categories ,
                                                "pro":pro ,
                                                "sub_total":sub_total,
                                                "discount_price":discount_price,
                                                "final_price":final_price,
                                                "counts":counts ,
                                                'status': status,
                                                "ord_counts":ord_counts,
                                                "cart_counts":cart_counts,
                                                })
        return redirect('login')
    
    #add_cart function to add Items/Products in cart
    def add_cart(request , id):
        if request.user.is_authenticated:
            user = request.user
            new = Product.objects.get(id = id)
            pro = Cart.objects.create(products = new, user = user)
            pro.save()
            return redirect('cart')
        return redirect('login')

    #success function to handle the payment successfull
    @csrf_exempt
    def success(request):
        url = request.GET.getlist('pending_ids') #get ids of items after successfull payment

        # Flatten the list of comma-separated IDs into a single list of integers
        # 1. `for i in url`: Iterate over the strings in the `url` list.
        # 2. `i.split(",")`: Split each string into a list of individual ID strings.
        # 3. `for id_str in i.split(",")`: Iterate over the split ID strings.
        # 4. `int(id_str)`: Convert each string ID to an integer.
        IdList = [int(id_str) for i in url for id_str in i.split(",")]

        for i in IdList:
            ChangeStatus = Cart.objects.get(id = i)
            ChangeStatus.ord_status = True
            ChangeStatus.save()
        messages.success(request ,f'Successfully Purchased')
        return redirect('cart')
    
    #delete function to delete the cart item
    def delete_product(request , id):
        if request.POST:
            Quan = request.POST.get('quantity')
            Ql = Cart.objects.get(id = id)
            if Ql.quantity == 1 or int(Quan) == Ql.quantity:
                Ql.delete()
                messages.success(request ,f"Removed Item from Cart")
                return redirect('cart')
            else:
                Ql.quantity -= int(Quan)
                Ql.save()
                return redirect('cart')
    
    #update function to update the quantity of the cart item        
    def update(request , id):
        if request.user.is_authenticated:
            if request.method == 'POST':
                quantity = request.POST.get('quantity')
                updt_item = Cart.objects.get(id = id)
                updt_item.quantity += int(quantity)
                updt_item.save()
                return redirect('cart')
        return redirect('login')
    
    #uncart function to delete the cart item which are ordered
    def Uncart(request):
        item = request.GET.get('Id')
        print(f"Item Id :- {item}")
        Item_dlt = Cart.objects.get(id = item)
        Item_dlt.delete() #delete the cart item which is order
        return redirect('cart')



def cate(request): # Logic after Category is Clicked
    inp_get = request.GET.get('categories')
    categories = Category.objects.all()
    s_category = Com.objects.filter(ct__name = inp_get)
    product = Product.objects.filter(category__name = inp_get)
    counts = Cart.objects.all().count()-1
    return render(request , "category.html", {"categories":categories,'product':product,"s_category":s_category,"counts":counts})

# Logic after Sub-Category is Clicked
def sub_category(request , id):
    categories = Category.objects.all()
    product = Product.objects.filter(brand = id)
    counts = Cart.objects.all().count()-1
    return render(request , "category.html" , {"categories":categories ,
                                        'product':product ,
                                        "counts":counts})

def logout_user(request): # Logout Page
    logout(request)
    return redirect('login')


def products_all(request , id): # Logic after View option is Clicked on product
    categories = Category.objects.all()

    counts = Cart.objects.all().count()-1

    products = Product.objects.get(id = id)

    product = Product.objects.filter(category = products.category).exclude(id = id)[:4]

    return render(request , "product.html",{'products':products ,
                                            "categories":categories ,
                                             'product':product,
                                             "counts":counts})
  

def about(request):
    categories = Category.objects.all()
    counts = Cart.objects.all().count()-1
    return render (request , "about.html",{"categories":categories ,"counts":counts})

def slider(request):
    categories = Category.objects.all()
    all =Product.objects.all() 
    return render (request , "slider.html",{"categories":categories ,"all":all })

def MyProfile(request): #function to display user profile and update
    if request.user.is_authenticated:
        categories = Category.objects.all()
        counts = max(0, Cart.objects.all().count()-1)
        if request.POST:
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            username = request.POST.get("username")
            email = request.POST.get("email")

            fields_to_update = {}
            if firstname:
                fields_to_update['first_name'] = firstname
            if lastname:
                fields_to_update['last_name'] = lastname
            if username:
                if User.objects.filter(username__iexact=username).exists():
                    messages.error(request, "Username already exists")
                else:
                    fields_to_update['username'] = username
            if email:
                if User.objects.filter(email__iexact=email).exists():
                    messages.error(request, "Email already exists")
                else:
                    fields_to_update['email'] = email

            if fields_to_update:
                User.objects.filter(username=request.user.username).update(**fields_to_update)
                lst = '<br>'.join([f"<b>{key}</b>: {value}" for key, value in fields_to_update.items()])
                messages.success(request, mark_safe(f"Successfully Updated<br>{lst}"))
                return redirect("my_profile")
        return render(request, "my_profile.html", {"categories":categories, "counts":counts})
    return redirect('login')
