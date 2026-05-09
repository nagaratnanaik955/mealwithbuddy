from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_home/', views.user_home, name='user_home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_restaurant, name='add_restaurant'),
    path('view/', views.view_restaurants, name='view_restaurants'),
    path('manage/', views.manage_restaurants, name='manage_restaurants'),
    path('menu/<str:restaurant_name>/', views.view_menu, name='view_menu'),
    path('menu/manage/<str:restaurant_name>/', views.manage_menu, name='manage_menu'),
    path('add_to_cart/<int:restaurant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<str:username>/', views.view_cart, name='view_cart'),
    path('edit/<str:restaurant_name>/', views.edit_restaurant, name='edit_restaurant'),
    path('delete/<str:restaurant_name>/', views.delete_restaurant, name='delete_restaurant'),
    path('menu_item/add/<str:restaurant_name>/', views.add_menu_item, name='add_menu_item'),
    path('menu_item/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu_item/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('checkout/<str:username>/', views.checkout, name='checkout'),
]
