from django.urls import path, include
from . import views


urlpatterns = [
    #Default URL
    path('', views.home, name='home'),
    #Store
    path('about/', views.about, name='about'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    #Auth
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    #User
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_info/', views.user_info, name='user_info'),
    path('update_password/', views.update_password, name='update_password'),
    #Admin
    path('admin_categories/', views.admin_categories, name='admin_categories'),
    path('update_categories/', views.update_categories, name='update_categories'),
    path('add_categories/', views.add_categories, name='add_categories'),
    path('delete_categories/', views.delete_categories, name='delete_categories'),
    path('admin_products/', views.admin_products, name='admin_products'),
    path('update_products/', views.update_products, name='update_products'),
    path('add_products/', views.add_products, name='add_products'),
    path('delete_products/', views.delete_products, name='delete_products'),
]
