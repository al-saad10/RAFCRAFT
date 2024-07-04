from django.shortcuts import render,redirect
from django.views import View
from django.shortcuts import HttpResponse
from django.contrib import messages
from .forms import MyPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.views import View
from .models import *
from .forms import *


# Create your views here.


    
class ChangePassword(LoginRequiredMixin,View):
    def get(self, request):
        form = MyPasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form': form})
    
    def post(self, request):
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update the user's session authentication hash to prevent logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('change_password')  # Redirect back to the same page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
            return redirect('change_password')


class CreateCustomUserProfile(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomUserProfileForm()
        profile = CustomUserProfile.objects.filter(user=request.user).first()
        if profile:
            return render(request, 'account/profile.html', {'form': form, 'profile': profile, 'active': 'btn-primary'})
        else:
            return render(request, 'account/profile.html', {'form': form, 'active': 'btn-primary'})
    

    def post(self, request):
        form = CustomUserProfileForm(request.POST)
        user=request.user
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            gender = form.cleaned_data['gender']

            # Checking if a profile already exists for the current user
            if CustomUserProfile.objects.filter(user=request.user).exists():
                profile = CustomUserProfile.objects.get(user=user)
                profile.first_name = first_name
                profile.last_name = last_name
                profile.phone = phone
                profile.email = email
                profile.country = country
                profile.street = street
                profile.city = city
                profile.gender = gender
                profile.save()
            else:
                profile = CustomUserProfile(user=user,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            phone=phone,
                                            country=country,
                                            street=street,
                                            city=city,
                                            gender=gender
                                            )
                profile.save()
            messages.success(request, 'Congratulations!! Profile Update Successfully')
        return redirect('profile')




