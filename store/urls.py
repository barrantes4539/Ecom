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
    path('update_password/', views.update_password, name='update_password'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
