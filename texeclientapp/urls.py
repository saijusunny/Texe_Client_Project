from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('product_view',views.product_view, name='product_view'),

    
]