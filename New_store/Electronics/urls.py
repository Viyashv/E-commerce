

# from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', home , name='home'),
    path('login/', login , name='login'),
    path('register/', register , name='register'),
    path('logout/', logout_user , name='logout'),
    path('cart/', cart , name='cart'),
    path('add/<int:id>', add_cart , name='add'),
    path('delete/<int:id>', delete_product , name='delete'),
    path('category/<int:id>', cate , name='category'),
    path('sub_category/<int:id>', sub_category , name='sub_category'),
    path('product/<int:id>', products_all , name='product'),
    path('about/', about , name='about'),
    path('slider/', slider , name='slider'),
    path('update/<int:id>', update , name='update'),
    path('cart/paymenthandler/', success , name='success'),
    path('search/', search_view, name='search'),
    # path('pay/', pay , name='pay'),
]
