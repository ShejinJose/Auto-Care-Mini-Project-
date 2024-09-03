from . import views 
from .views import  delete_customer, service_manager_list, delete_service_manager
from django.urls import path


urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'), 
    path('contact',views.contact,name='contact'),
    path('customerLogin',views.cust_login,name='customerLogin'),
    path('customerRegister',views.cust_register,name='customerRegister'),
    path('add_vehicle', views.add_vehicle, name='add_vehicle'),
    path('logout',views.logout_view,name="logout"),
    path('location',views.location,name="location"),
    path('price',views.price),
    path('service',views.service,name="service"),
    path('booking',views.booking,name="booking"),
    path('cst_admin',views.cst_admin,name="cst_admin"),
    path('serviceManager',views.serviceManager,name="serviceManager"),
    path('customerdetails',views.customerdetails,name = 'customerdetails'),
    path('delete_customer/<str:email>/',delete_customer, name='delete_customer'),
    path('service_manager_list/', service_manager_list, name='service_manager_list'),
    path('delete_service_manager/<str:email>/', delete_service_manager, name='delete_service_manager'),
    path('add_service_manager/', views.add_service_manager, name='add_service_manager'),
    path('mechanic_list/', views.mechanic_list, name='mechanic_list'),
    path('delete_mechanic/<str:email>/', views.delete_mechanic, name='delete_mechanic'),
    path('add_mechanic/', views.add_mechanic, name='add_mechanic'),

]