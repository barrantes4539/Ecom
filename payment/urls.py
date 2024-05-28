from django.urls import path, include
from . import views


urlpatterns = [
    #Payment
    path('payment_success', views.payment_success, name='payment_success'),
]
