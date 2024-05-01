from django.urls import path, include
from . import views

urlpatterns = [
    #Default URL
    path('', views.home, name='home'),
    #Auth
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    #Store
    path('about/', views.about, name='about'),
    path('product/<int:pk>', views.product, name='product'),
]
