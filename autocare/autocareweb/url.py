from . import views 
from .views import  delete_customer, service_manager_list, delete_service_manager
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


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
    path('mechanic',views.mechanic,name="mechanic"),

    #///////////////  Vehicle Select /////////////
    path('select-vehicle/', views.select_vehicle, name='select_vehicle'),
    path('add_vehicle_number/<int:variant_id>/', views.add_vehicle_number, name='add_vehicle_number'),
     path('vehicle-brand/', views.vehicle_brand, name='vehicle_brand'),

    # URL for displaying variants of a selected brand
    # path('brand-variants/<int:brand_id>/', views.brand_variants, name='brand_variants'),
    path('brand/<int:brand_id>/variants/', views.vehicle_variants, name='vehicle_variants'),


    # path('add-vehicle/', views.add_vehicle, name='add_vehicle'),

    #///////////////   Password Reset///////////////////////

    path('password-reset/', 
        views.CustomPasswordResetView.as_view(
            template_name='password/password_reset.html',
            email_template_name='password/password_reset_email.html',
            subject_template_name='password/password_reset_subject.txt'
        ),
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='password/password_reset_done.html'
        ),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password/password_reset_confirm.html'
        ),
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password/password_reset_complete.html'
        ),
        name='password_reset_complete'),


        #///////////////////  change password ///////////////////
    path('change-password/', views.change_password, name='change_password'),


    #/////////Admin Dashboard///////////
    path('cst_admin',views.cst_admin,name="cst_admin"),
    path('customerdetails',views.customerdetails,name = 'customerdetails'),
    path('delete_customer/<str:email>/',delete_customer, name='delete_customer'),
    path('service_manager_list/', service_manager_list, name='service_manager_list'),
    path('delete_service_manager/<str:email>/', delete_service_manager, name='delete_service_manager'),
    path('add_service_manager/', views.add_service_manager, name='add_service_manager'),
    path('mechanic_list/', views.mechanic_list, name='mechanic_list'),

    path('mechanics/update_level/<int:mechanic_id>/', views.update_mechanic_level, name='update_mechanic_level'),

    path('delete_mechanic/<str:email>/', views.delete_mechanic, name='delete_mechanic'),
    path('add_mechanic/', views.add_mechanic, name='add_mechanic'),
    path('cst_admin/vehicle-make/create/', views.create_vehicle_make, name='create_vehicle_make'),
    path('cst_admin/vehicle-model/create/', views.create_vehicle_model, name='create_vehicle_model'),
    path('cst_admin/manage_vehicle', views.manage_vehicle, name='manage_vehicle'),
    path('brands/<int:brand_id>/add_variant/', views.add_vehicle_model, name='add_variant'),
    path('cst_admin/manage_vehicle/<int:brand_id>/brand_variants/', views.brand_variants, name='brand_variants'),
    path ('cst_admin/addSlot/', views.manageSlot ,name='addslot'),
    # path ('cst_admin/slot_list/', views.Slotlist ,name='slot_list'),
    path('cst_admin/slots/', views.slot_list, name='slot_list'),
    path('allocate-manager/<slug:slug>/', views.allocate_manager, name='allocate_manager'),


    #/////////// Service Manager /////////////////////////////////////////

    path('serviceManager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/allocate_mechanic/<slug:slot_slug>/', views.allocate_mechanic, name='allocate_mechanic'),





    #////////////////////// Service Categories/////////////////////////////////
    path('cst_admin/service-categories/', views.service_category_list, name='service_category_list'),
    path('cst_admin/service-categories/edit/<int:pk>/', views.edit_service_category, name='edit_service_category'),
    path('cst_admin/service-categories/delete/<int:pk>/', views.delete_service_category, name='delete_service_category'),

    #////////////////   Service Types /////////////////////////////////////
    path('cst_admin/service-categories/<int:category_id>/service-types/', views.service_type_list, name='service_type_list'),
    path('cst_admin/service-types/edit/<int:pk>/', views.edit_service_type, name='edit_service_type'),
    path('cst_admin/service-types/delete/<int:pk>/', views.delete_service_type, name='delete_service_type'),

   
    #////////////////////   CUSTOMER PROFILE ///////////////
     path('customer_profile/', views.customer_profile, name='customer_profile'),
      path('profile/edit/', views.edit_profile, name='edit_profile'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)