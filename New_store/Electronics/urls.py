from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

# from django.contrib import admin
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
    path('products/', sort_products, name='sort_products'),
        # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('pay/', pay , name='pay'),
]
