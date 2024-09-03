from . import views 
from .views import customerdetails,  delete_customer
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'), 
    path('contact',views.contact,name='contact'),
    path('customerLogin',views.cust_login,name='customerLogin'),
    path('customerRegister',views.cust_register,name='customerRegister'),
    path('logout',views.logout_view,name="logout"),
    path('location',views.location,name="location"),
    path('price',views.price),
    path('service',views.service,name="service"),
    path('booking',views.booking,name="booking"),
    path('cst_admin',views.cst_admin,name="cst_admin"),
    path('serviceManager',views.serviceManager,name="serviceManager"),
    path('customerdetails',views.customerdetails,name = 'customerdetails'),
    path('delete_customer/<str:email>/', delete_customer, name='delete_customer'),
]