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
  
    #---------------------------------------------------------------------------------User Module
    path('product_view/<int:id>',views.product_view, name='product_view'),
    path('cust',views.cust, name='cust'),
    path('all_item',views.all_item, name='all_item'),
    path('carts',views.carts, name='carts'),
    path('whistle',views.whistle, name='whistle'),
    path('my_order',views.my_order, name='my_order'),
    path('profile',views.profile, name='profile'),
    path('edit_user_profile/<int:id>',views.edit_user_profile, name='edit_user_profile'),
    path('checkout',views.checkout, name='checkout'),
    path('add_wishlist',views.add_wishlist, name='add_wishlist'),
    path('cart_cust_size',views.cart_cust_size, name='cart_cust_size'),
    path('cart_change_color',views.cart_change_color, name='cart_change_color'),
    path('cart_change_meterial',views.cart_change_meterial, name='cart_change_meterial'),
    path('cart_change_model',views.cart_change_model, name='cart_change_model'),
    path('save_cart/<int:id>',views.save_cart, name='save_cart'),
    path('cancel_order/<int:id>',views.cancel_order, name='cancel_order'),
    path('remove_wishlist/',views.remove_wishlist, name='remove_wishlist'),
    path('search',views.search, name='search'),
    path('get_items',views.get_items, name='get_items'),
    path('show_category/<int:id>',views.show_category, name='show_category'),
    path('delete_cart/<int:id>',views.delete_cart, name='delete_cart'),
    path('get_location',views.get_location, name='get_location'),
    #--------------------------------------------------------------------------admin Module
    path('admin_home',views.admin_home, name='admin_home'),
    path('create_banner',views.create_banner, name='create_banner'),
    path('all_events',views.all_events, name='all_events'),

    path('add_event',views.add_event, name='add_event'),
    path('update',views.update, name='update'),
    path('remove',views.remove, name='remove'),
    path('create_banner',views.create_banner, name='create_banner'),
    path('save_banner',views.save_banner, name='save_banner'),
    path('edit_banner/<int:id>',views.edit_banner, name='edit_banner'),
    path('edit_category/<int:id>',views.edit_category, name='edit_category'),
    path('admin_subcategory',views.admin_subcategory, name='admin_subcategory'),
    path('admin_category',views.admin_category, name='admin_category'),
    path('admin_save_category',views.admin_save_category, name='admin_save_category'),
    path('ad_category_list',views.ad_category_list, name='ad_category_list'),
    path('delete_cat/<int:id>',views.delete_cat, name='delete_cat'),
    path('edit_subcategory/<int:id>',views.edit_subcategory, name='edit_subcategory'),
    path('product',views.product, name='product'),
    path('admin_add_item',views.admin_add_item, name='admin_add_item'),
    path('edit_item/<int:id>',views.edit_item, name='edit_item'),
    path('order',views.order, name='order'),
    path('change_order_status',views.change_order_status, name='change_order_status'),
    path('order_details/<int:id>',views.order_details, name='order_details'),    
    path('delivery_orders',views.delivery_orders, name='delivery_orders'),
    path('delivery_order_details/<int:id>',views.delivery_order_details, name='delivery_order_details'),
    path('admin_ad_category',views.admin_ad_category, name='admin_ad_category'), 
    path('remove_sub_cat',views.remove_sub_cat, name='remove_sub_cat'),
    path('user_list_view',views.user_list_view, name='user_list_view'),
    path('delete_user/<int:id>',views.delete_user, name='delete_user'), 
    path('export_user_excel',views.export_user_excel, name='export_user_excel'),
    path('deactive_user/<int:id>',views.deactive_user, name='deactive_user'),
    path('active_user/<int:id>',views.active_user, name='active_user'),
    path('filter_order',views.filter_order, name='filter_order'),
    path('filter_delivery',views.filter_delivery, name='filter_delivery'),
    path('filter_order_id',views.filter_order_id, name='filter_order_id'),
    path('filter_delivery_id',views.filter_delivery_id, name='filter_delivery_id'),
    
    
]