from . import views 
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about),
    path('contact',views.contact),
    path('customerLogin',views.cust_login),
    path('customerRegister',views.cust_register),
    path('location',views.location),
    path('price',views.price),
    path('service',views.service),
    path('booking',views.booking),
]