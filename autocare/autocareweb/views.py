from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from .form import CustomUserCreationForm, UserDetailsForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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
                    return redirect('admin/')
                elif user.role == 'service_manager':
                    return redirect('serviceManager/')
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
            return redirect('customerLogin')  
    else:
        user_form = CustomUserCreationForm()
        details_form = UserDetailsForm()
    return render(request,"cust_register.html",{'user_form': user_form, 'details_form': details_form})


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
    return render(request,'serviceManager\managerhome.html')
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