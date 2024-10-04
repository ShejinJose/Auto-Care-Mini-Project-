from . import views 
from .views import  delete_customer, service_manager_list, delete_service_manager
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


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
    path('serviceManager',views.serviceManager,name="serviceManager"),
    path('mechanic',views.mechanic,name="mechanic"),
    #/////////Admin Dashboard///////////
    path('cst_admin',views.cst_admin,name="cst_admin"),
    path('customerdetails',views.customerdetails,name = 'customerdetails'),
    path('delete_customer/<str:email>/',delete_customer, name='delete_customer'),
    path('service_manager_list/', service_manager_list, name='service_manager_list'),
    path('delete_service_manager/<str:email>/', delete_service_manager, name='delete_service_manager'),
    path('add_service_manager/', views.add_service_manager, name='add_service_manager'),
    path('mechanic_list/', views.mechanic_list, name='mechanic_list'),
    path('delete_mechanic/<str:email>/', views.delete_mechanic, name='delete_mechanic'),
    path('add_mechanic/', views.add_mechanic, name='add_mechanic'),
    path('cst_admin/vehicle-make/create/', views.create_vehicle_make, name='create_vehicle_make'),
    path('cst_admin/vehicle-model/create/', views.create_vehicle_model, name='create_vehicle_model'),
    path('cst_admin/manage_vehicle', views.manage_vehicle, name='manage_vehicle'),
    path('brands/<int:brand_id>/add_variant/', views.add_vehicle_model, name='add_variant'),
    path('cst_admin/manage_vehicle/<int:brand_id>/brand_variants/', views.brand_variants, name='brand_variants'),


    #////////////////////// Service Categories/////////////////////////////////
    path('service-categories/', views.service_category_list, name='service_category_list'),
    #////////////////////// Service Types/////////////////////////////////
    path('categories/<int:category_id>/types/', views.service_type_list, name='service_type_list'),
    #////////////////////   CUSTOMER PROFILE ///////////////
     path('customer_profile/', views.customer_profile, name='customer_profile'),
      path('profile/edit/', views.edit_profile, name='edit_profile'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)