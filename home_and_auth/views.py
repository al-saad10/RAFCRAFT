from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import *
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import  messages
from django.views.generic import View
from django.shortcuts import render
from .models import SliderItem
from products.models import *
from django.contrib.auth import logout as django_logout

class Master(View):
    def get(self, request):
        return render(request, "master.html")

class MY_Account(View):
    def get(self, request):
        return render(request, "acc.html")

class Register(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        # Handle POST request for user registration
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("login")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("login")


        # Create a new user object with the provided username, email, and password
        user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password)

        user.save()
        return redirect("login")

class Login(View):

    def post(self, request):
        # Handle POST request for user registration
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user is not user.is_superuser:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

def logout(request):
    django_logout(request)
    return redirect('index')

class HomeView(View):
    def get(self, request):
        slider_items = SliderItem.objects.all()
        subcategories = SubCategory.objects.all()
        new_arrivals = Product.objects.prefetch_related('images').all().order_by('-id')[:8]
        categories = Category.objects.all()
        return render(request, 'home/index.html', {'slider_items': slider_items, 'subcategories': subcategories,'categories':categories, 'new_arrivals': new_arrivals})
    
class AboutUs(View):
    def get(self, request):
        return render(request, 'home/about.html')







