from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')
def about(request) :
    return render(request,"about.html")
def contact(request) :
    return render(request,"contact.html")
def cust_login(request) :
    return render(request,"cust_login.html")
def cust_register(request) :
    return render(request,"cust_register.html")
def price(request) :
    return render(request,"price.html")
def service(request) :
    return render(request,"service.html")
def booking(request) :
    return render(request,"booking.html")
def location(request) :

    return render(request,"location.html")


