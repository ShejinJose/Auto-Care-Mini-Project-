from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .form import CustomUserCreationForm, UserDetailsForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
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



#////////////////  Password Reset /////////////////////////////
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import CustomUser

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password/password_reset.html'
    email_template_name = 'password/password_reset_email.html'
    subject_template_name = 'password/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email has been sent with instructions to reset your password"
    
    def form_valid(self, form):
        # """
        # Validates the form and checks if the email exists in the database
        # """
        email = form.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "This email address is not registered with us.")
            return self.form_invalid(form)
        return super().form_valid(form)
    

    #///////////////////  Change Password ///////////////////////


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # Saves the new password
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')  # Redirect to the profile page or desired page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


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


def select_vehicle(request):
    user = request.user
    vehicles = Vehicle.objects.filter(user=user)

    if request.method == 'POST':
        selected_vehicle_id = request.POST.get('selected_vehicle')
        if selected_vehicle_id:
            selected_vehicle = get_object_or_404(Vehicle, id=selected_vehicle_id, user=user)
            # You can now do something with the selected vehicle, like setting it as the current vehicle in the session
            request.session['selected_vehicle_id'] = selected_vehicle.id
            return redirect('home')  # Redirect to wherever you need after selection

    return render(request, 'vehicle/select_vehicle.html', {'vehicles': vehicles})


# def add_vehicle(request):
#     if request.method == 'POST':
#         form = AddVehicleForm(request.POST)
#         if form.is_valid():
#             vehicle = form.save(commit=False)
#             vehicle.user = request.user
#             vehicle.save()
#             return redirect('select_vehicle')  # Redirect to select vehicle after adding
#     else:
#         form = AddVehicleForm()

#     return render(request, 'vehicle/add_vehicle.html', {'form': form})

from .form import VehicleForm

def vehicle_brand(request):
    vehicle_makes = VehicleMake.objects.all()  # Fetch all vehicle makes (brands)
    return render(request, 'vehicle/vehicle_brand.html', {'vehicle_makes': vehicle_makes})

# View to display variants for a selected brand
def vehicle_variants(request, brand_id):
    brand = get_object_or_404(VehicleMake, id=brand_id)  # Fetch the selected brand by ID
    variants = VehicleModel.objects.filter(make=brand)  # Fetch all variants related to the selected brand
    return render(request, 'vehicle/vehicle_variants.html', {'brand': brand, 'variants': variants})


def add_vehicle_number(request, variant_id):
    vehicle_variant = get_object_or_404(VehicleModel, id=variant_id)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            
            # Check if the registration number already exists
            if Vehicle.objects.filter(registration_number=registration_number).exists():
                error_message = "This registration number is already registered."
                return render(request, 'vehicle/add_vehicle_number.html', {
                    'vehicle_variant': vehicle_variant,
                    'form': form,
                    'error_message': error_message
                })

            # Create and save the new vehicle
            vehicle = Vehicle.objects.create(
                user=request.user,
                vehicle_model=vehicle_variant,
                registration_number=registration_number
            )
            vehicle.save()

            # Redirect to some success page or homepage
            return redirect('home')  # Or wherever you want to redirect
    
    else:
        form = VehicleForm()

    return render(request, 'vehicle/add_vehicle_number.html', {
        'vehicle_variant': vehicle_variant,
        'form': form
    })






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

    # Retrieve the slots assigned to the service manager
    assigned_slots = AllocatedManager.objects.filter(manager=manager)

    # Initialize the mechanic variable
    mechanic = None  # Set mechanic to None initially

    if request.method == 'POST':
        form = AssignMechanicForm(request.POST)
        if form.is_valid():
            slot_id = form.cleaned_data['slot_id']
            mechanic = form.cleaned_data['mechanic']

            # Assign the mechanic to the selected slot
            slot = Slot.objects.get(id=slot_id)
            slot.mechanic = mechanic
            slot.save()

            return redirect('manager_dashboard')  # Refresh the dashboard after assigning the mechanic
    else:
        form = AssignMechanicForm()

    return render(
        request, 
        'serviceManager/dashboard.html', 
        {
            'assigned_slots': assigned_slots,
            'mechanic': mechanic,  # mechanic will be None in GET requests
            'form': form,
            'user': request.user
        }
    )




def allocate_mechanic(request):
    if request.method == "POST":
        form = MechanicAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
    else:
        form = MechanicAllocationForm()
    return render(request, 'manager_dashboard', {'form': form})

# def reallocate_mechanic(request, allocation_id):
#     allocation = get_object_or_404(AllocatedMechanic, id=allocation_id)
#     if request.method == "POST":
#         form = MechanicAllocationForm(request.POST, instance=allocation)
#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard')
#     else:
#         form = MechanicAllocationForm(instance=allocation)
#     return render(request, 'serviceManager/reallocate_mechanic.html', {'form': form})





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


# def mechanics_list(request):
#     mechanics = Mechanic.objects.all()
#     return render(request, 'mechanics_list.html', {'mechanics': mechanics})

# View for updating mechanic level
def update_mechanic_level(request, mechanic_id):
    mechanic = get_object_or_404(Mechanic, mechanic_id=mechanic_id)
    
    if request.method == 'POST':
        selected_level = request.POST.get('level')
        mechanic.level = selected_level
        mechanic.save()
        
        messages.success(request, 'Mechanic level updated successfully.')
        return redirect('mechanic_list')

    return redirect('mechanic_list')



#////////////////////Service Categories Adding by admin///////////////////////////////////

def service_category_list(request):
    service_categories = ServiceCategory.objects.all()

    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_category_list')

    form = ServiceCategoryForm()

    return render(request, 'admin/service/service_category_list.html', {
        'service_categories': service_categories,
        'form': form
    })

def edit_service_category(request, pk):
    service_category = get_object_or_404(ServiceCategory, pk=pk)

    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES, instance=service_category)
        if form.is_valid():
            form.save()
            return redirect('service_category_list')

    form = ServiceCategoryForm(instance=service_category)

    return render(request, 'admin/service/edit_service_category.html', {
        'form': form,
        'service_category': service_category
    })

def delete_service_category(request, pk):
    service_category = get_object_or_404(ServiceCategory, pk=pk)
    if request.method == 'POST':
        service_category.delete()
        messages.success(request, f'Service category "{service_category.name}" has been deleted.')
        return redirect('service_category_list')
    return render(request, 'admin/service/delete_service_category.html', {'service_category': service_category})

#///////////////////   Service Types by Admin ?////////////////////

# views.py


# View to display service types for a specific category
def service_type_list(request, category_id):
    category = get_object_or_404(ServiceCategory, pk=category_id)
    service_types = category.service_types.all()  # Fetch related service types
    
    # If the form is being submitted
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, request.FILES)
        if form.is_valid():
            service_type = form.save(commit=False)
            service_type.category = category
            service_type.save()
            messages.success(request, 'Service type added successfully.')
            return redirect('service_type_list', category_id=category_id)
    else:
        form = ServiceTypeForm()

    # Render the page with service types and the form for adding service types
    return render(request, 'admin/service/service_type_list.html', {
        'category': category,
        'service_types': service_types,
        'form': form  # Pass the form to the template
    })

# View to edit a service type
def edit_service_type(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, request.FILES, instance=service_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service type updated successfully.')
            return redirect('service_type_list', category_id=service_type.category.pk)
    else:
        form = ServiceTypeForm(instance=service_type)
    return render(request, 'admin/service/edit_service_type.html', {'form': form, 'service_type': service_type})

# View to delete a service type
def delete_service_type(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    category_id = service_type.category.pk
    if request.method == 'POST':
        service_type.delete()
        messages.success(request, 'Service type deleted successfully.')
        return redirect('service_type_list', category_id=category_id)
    return render(request, 'admin/service/delete_service_type.html', {'service_type': service_type})


