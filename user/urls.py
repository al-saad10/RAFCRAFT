from django.urls import path
from .views import *



urlpatterns = [
        path('profile/', CreateCustomUserProfile.as_view(), name='profile'),
        path('change_password/', ChangePassword.as_view(), name='change_password')
]