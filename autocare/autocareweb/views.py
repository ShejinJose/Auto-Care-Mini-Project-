from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .form import CustomUserCreationForm, UserDetailsForm,  VehicleForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser, UserDetails, Vehicle

# Create your views here.
def home(request):
    user = request.user
    return render(request,'index.html',{'user' : user})
def about(request) :
    return render(request,"about.html")
def contact(request) :
    return render(request,"contact.html")
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
                    return redirect('serviceManager')
                elif user.role == 'mechanic':
                     return redirect('mechanics')
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
            return redirect('add_vehicle')  
    else:
        user_form = CustomUserCreationForm()
        details_form = UserDetailsForm()
    return render(request,"cust_register.html",{'user_form': user_form, 'details_form': details_form})


#///////////////////////////   ADD VEHICLES   /////////////////////////////////////////////

def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('customerLogin')  # Redirect to the list of vehicles after successful submission
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})


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



#/////////////////Service Manager Dashboard/////////////////////////
def serviceManager(request):
    
    return render(request,'serviceManager/managerhome.html')
"""
from django.shortcuts import render, redirect
from .models import Customer, Mechanic, Feedback, Complaint
from .forms import AlertForm

def service_manager_dashboard(request):
    customers = Customer.objects.all()
    mechanics = Mechanic.objects.all()
    feedbacks = Feedback.objects.all()
    complaints = Complaint.objects.all()

    if request.method == 'POST':
        alert_form = AlertForm(request.POST)
        if alert_form.is_valid():
            alert_form.save()  # Save the alert and notify the mechanic
            messages.success(request, 'Alert sent successfully!')
            return redirect('service_manager_dashboard')
    else:
        alert_form = AlertForm()

    context = {
        'customers': customers,
        'mechanics': mechanics,
        'feedbacks': feedbacks,
        'complaints': complaints,
        'alert_form': alert_form,
    }
    
    return render(request, 'service_manager_dashboard.html', context)

"""
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