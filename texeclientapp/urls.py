from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('forgotPassword/', views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword,name='resetPassword'),
    path('product_view',views.product_view, name='product_view'),
    path('cust',views.cust, name='cust'),
    path('all_item',views.all_item, name='all_item'),
    path('cart',views.cart, name='cart'),
    path('whistle',views.whistle, name='whistle'),
    path('my_order',views.my_order, name='my_order'),
    path('profile',views.profile, name='profile'),
    path('edit_user_profile/<int:id>',views.edit_user_profile, name='edit_user_profile'),

    #--------------------------------------------------------------------------admin Module
    path('admin_home',views.admin_home, name='admin_home'),
    path('create_banner',views.create_banner, name='create_banner'),
    path('ex_add_event',views.ex_add_event, name='ex_add_event'),
    path('ex_update',views.ex_update, name='ex_update'),
    path('ex_remove',views.ex_remove, name='ex_remove'),

    
]