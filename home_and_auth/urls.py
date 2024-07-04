from django.urls import path
from home_and_auth.views import *
from django.urls import path, include



urlpatterns = [
        path('master/', Master.as_view(), name='master_view'),
        path('',HomeView.as_view(),name='index'),
        path('about/', AboutUs.as_view(), name='about'),
        #path('signup',Signup.as_view(),name='signup'),
        #account urls
        path('account/my-account',MY_Account.as_view(),name='my_account'),
        path('account/register',Register.as_view(),name='handle_register'),
        path('account/login',Login.as_view(),name='handle_login'),
        path('accounts/', include('django.contrib.auth.urls')),
        path('logout/', logout, name='logout'),
        # path('social-auth/', include('social_django.urls', namespace='social')),




]