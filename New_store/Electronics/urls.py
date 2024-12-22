from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib import admin

# from django.contrib import admin
urlpatterns = [
    path('', HomePageView.home , name='home'),
    path('admin/', admin.site.urls),
    path('login/', login , name='login'),
    path('register/', register , name='register'),
    path('logout/', logout_user , name='logout'),
    path('cart/', CartPageViews.cart , name='cart'),
    path('add/<int:id>', CartPageViews.add_cart , name='add'),
    path('delete/<int:id>', CartPageViews.delete_product , name='delete'),
    path('category/', CategoryPageViews.cate , name='category'),
    path('sub_category/<int:id>', CategoryPageViews.sub_category , name='sub_category'),
    path('product/<int:id>', products_all , name='product'),
    path('about/', about , name='about'),
    path('slider/', slider , name='slider'),
    path('update/<int:id>', CartPageViews.update , name='update'),
    path('cart/paymenthandler/', CartPageViews.success , name='success'),
    path('search/', HomePageView.search_view, name='search'),
    path('products/', HomePageView.sort_products, name='sort_products'),
    path('uncart/', CartPageViews.Uncart, name='uncart'),
    path('profile/', MyProfile, name='my_profile'),
        # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
