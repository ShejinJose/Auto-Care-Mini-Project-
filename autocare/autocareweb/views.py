from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .form import CustomUserCreationForm, UserDetailsForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from .form import *

# Create your views here.
def home(request):
    user = request.user
    return render(request,'index.html',{'user' : user})
def about(request) :
    return render(request,"about.html")
def contact(request) :
    return render(request,"contact.html")

#//////////////////////////CUSTOMER LOGIN  /////////////////////////////
def cust_login(request) :
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in.')
                if user.role == 'admin':
                    return redirect('cst_admin')
                elif user.role == 'service_manager':
                    return redirect('manager_dashboard')
                elif user.role == 'mechanic':
                     return redirect('mechanic')
                elif user.role == 'customer':
                     return redirect('home')


                  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()
    return render(request,"cust_login.html",{'form': form})


#//////////////////////////  Registration Views ///////////////////////////////////////

def cust_register(request) :
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        details_form = UserDetailsForm(request.POST)
        if user_form.is_valid() and details_form.is_valid():
            user = user_form.save()
            details = details_form.save(commit=False)
            details.user = user
            details.save()
            messages.success(request, 'Registered Successfully.')
            login(request, user)
            return redirect('customerLogin')  
    else:
        user_form = CustomUserCreationForm()
        details_form = UserDetailsForm()
    return render(request,"cust_register.html",{'user_form': user_form, 'details_form': details_form})


#///////////////////////////   ADD VEHICLES   /////////////////////////////////////////////

# def add_vehicle(request):
#     if request.method == 'POST':
#         form = VehicleForm(request.POST)
#         if form.is_valid():
#             vehicle = form.save(commit=False)
#             vehicle.owner = request.user
#             vehicle.save()
#             return redirect('customerLogin')  # Redirect to the list of vehicles after successful submission
#     else:
#         form = VehicleForm()
#     return render(request, 'add_vehicle.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')

def price(request) :
    return render(request,"price.html")
def service(request) :
    return render(request,"service.html")
def booking(request) :
    return render(request,"booking.html")
def location(request) :
    return render(request,"location.html")


def cst_admin(request):
    return render(request,'admin/dashboard.html')

from django.shortcuts import render, redirect
from .form import VehicleMakeForm, VehicleModelForm

def create_vehicle_make(request):
    if request.method == 'POST':
        form = VehicleMakeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vehicle_make_success')  # Redirect to a success page or list view
    else:
        form = VehicleMakeForm()

    return render(request, 'admin/vehicle_make_form.html', {'form': form})

def create_vehicle_model(request):
    if request.method == 'POST':
        form = VehicleModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vehicle_model_success')  # Redirect to a success page or list view
    else:
        form = VehicleModelForm()

    return render(request, 'admin/add_vehicle_model.html', {'form': form})

def manage_vehicle(request) :
    vehicle_makes = VehicleMake.objects.all()
    return render(request, 'admin/manage_vehicle.html',{'vehicle_makes': vehicle_makes})


#//////////////// Slot List ????????????????????????????????????????????

# def Slotlist(request):
#     slots = Slot.objects.all() 
#     return render(request, 'admin/slot_list.html',  {'form': forms, 'slot': slots})

def manageSlot (request):
    if request.method == 'POST':
        form = SlotForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new slot to the database
            return redirect('slot_list')  # Redirect to the list of slots or a success page
    else:
        form = SlotForm()
    return render (request,"admin/addslot.html",{'form':form})

def slot_list(request):
    slots = Slot.objects.all()
    form = ManagerAllocationForm()

    context = {
        'slots': slots,
        'form': form
    }
    return render(request, 'admin/slot_list.html', context)


# def allocate_manager(request, slug):
#     slot = get_object_or_404(Slot, slug=slug)

#     if request.method == 'POST':
#         form = AllocateManagerForm(request.POST)
#         if form.is_valid():
#             # Create or update the allocated manager
#             AllocatedManager.objects.update_or_create(
#                 slot=slot,
#                 defaults={'manager': form.cleaned_data['manager']}
#             )
#             slot.status = SlotStatus.ALLOCATED  # Update the slot status
#             slot.save()
#             return redirect('slot_list')  # Redirect to the slot list
#     else:
#         form = AllocateManagerForm()  # Create a new form instance

#     return render(request, 'admin/addslot.html', {'form': form, 'slot': slot})

def allocate_manager(request, slug):
    slot = get_object_or_404(Slot, slug=slug)
    if request.method == 'POST':
        form = ManagerAllocationForm(request.POST)
        if form.is_valid():
            manager = form.cleaned_data.get('manager')
            AllocatedManager.objects.update_or_create(
                slot=slot,
                defaults={'manager': manager}
            )
            return redirect('slot_list')
    return redirect('slot_list')



#/////////////// add vehicle by admin ////////////////////

def add_vehicle_model(request, brand_id):
    brand = get_object_or_404(VehicleMake, id=brand_id)

    if request.method == 'POST':
        form = VehicleModelForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_model = form.save(commit=False)
            vehicle_model.make = brand  # Link the vehicle model to the selected brand
            vehicle_model.save()
            return redirect('brand_variants', brand_id=brand.id)  # Redirect to the brand variants page
    else:
        form = VehicleModelForm()

    return render(request, 'admin/add_vehicle_model.html', {'form': form, 'brand': brand})


def brand_variants(request, brand_id):
    brand = get_object_or_404(VehicleMake, id=brand_id)
    variants = VehicleModel.objects.filter(make=brand)
    return render(request, 'admin/brand_variants.html', {'brand': brand, 'variants': variants})


#////////////////////////// CUSTOMER PROFILE ////////////////////////
from django.contrib.auth.decorators import login_required

@login_required
def customer_profile(request):
    user_details = get_object_or_404(UserDetails, user=request.user)
    return render(request, 'customer_profile.html', {'user_details': user_details})

@login_required
def edit_profile(request):
    user_details = get_object_or_404(UserDetails, user=request.user)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user_details)
        if form.is_valid():
            form.save()
            return redirect('customer_profile')
    else:
        form = UserDetailsForm(instance=user_details)
    
    return render(request, 'edit_profile.html', {'form': form})





#/////////////////Service Manager Dashboard/////////////////////////

@login_required
def manager_dashboard(request):
    # Get the logged-in service manager
    manager = request.user

    # Retrieve the slot assigned to the service manager
    assigned_slots = AllocatedManager.objects.filter(manager=manager)

    return render(request, 'serviceManager/dashboard.html', {'assigned_slots': assigned_slots})

#/////////////////Mechanic Dashboard/////////////////////////
def mechanic(request):
    return render(request,'mechanics/mechanic_dashboard.html')


#/////////Customer details in Admin Page/////////////////////////////

def customerdetails(request):

    customers = CustomUser.objects.filter(role='customer').select_related('details')
    return render(request,'admin/customerdetails.html',{'customers':customers})


def delete_customer(request, email):
    customer = get_object_or_404(CustomUser, email=email)
    if request.method == "POST":
        customer.delete()
        return redirect('customerdetails')
    return render(request, 'customerdetails')

#/////////Service Manager details in Admin Page/////////////////////////////


def service_manager_list(request):
    managers = CustomUser.objects.filter(role='service_manager')  # Filter service managers
    return render(request, 'admin/service_manager_list.html', {'managers': managers})

def delete_service_manager(request, email):
    manager = get_object_or_404(CustomUser, email=email, role='service_manager')
    if request.method == "POST":
        manager.delete()
        return redirect('service_manager_list')
    return redirect('service_manager_list')

def add_service_manager(request) :
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        details_form = UserDetailsForm(request.POST)
        if user_form.is_valid() and details_form.is_valid():
            user = user_form.save()
            details = details_form.save(commit=False)
            details.user = user
            details.save()
            messages.success(request, 'Registered Successfully.')
            return redirect('service_manager_list')  
    else:
        user_form = CustomUserCreationForm()
        details_form = UserDetailsForm()
    return render(request,"admin/add_service_manager.html",{'user_form': user_form, 'details_form': details_form})


#/////////Mechanics details in Admin Page/////////////////////////////


def mechanic_list(request):
    mechanics = CustomUser.objects.filter(role='mechanic')  # Filter service managers
    return render(request, 'admin/mechanics_list.html', {'mechanics': mechanics})

def delete_mechanic(request, email):
    mechanic = get_object_or_404(CustomUser, email=email, role='mechanic')
    if request.method == "POST":
        mechanic.delete()
        return redirect('mechanic_list')
    return redirect('mechanic_list')

def add_mechanic(request) :
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        details_form = UserDetailsForm(request.POST)
        if user_form.is_valid() and details_form.is_valid():
            user = user_form.save()
            details = details_form.save(commit=False)
            details.user = user
            details.save()
            messages.success(request, 'Registered Successfully.')
            return redirect('mechanic_list')  
    else:
        user_form = CustomUserCreationForm()
        details_form = UserDetailsForm()
    return render(request,"admin/add_mechanic.html",{'user_form': user_form, 'details_form': details_form})



#////////////////////Service Categories///////////////////////////////////

def service_category_list(request):
    categories = ServiceCategory.objects.all()
    return render(request, 'service_category_list.html', {'categories': categories})

#////////////////////Service Types///////////////////////////////////

def service_type_list(request, category_id):
    category = get_object_or_404(ServiceCategory, id=category_id)
    service_types = category.service_types.all()
    return render(request, 'service_type_list.html', {'category': category, 'service_types': service_types})
