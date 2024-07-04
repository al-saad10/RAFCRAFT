from django.db import models
# Create your models here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SliderItem(models.Model):
    event = models.CharField(max_length=100)

    def __str__(self):
        return self.event

class SliderItemImage(models.Model):
    slider_item = models.ForeignKey(SliderItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='slider_images/')

    def __str__(self):
        return f"Image for {self.slider_item.event}"





# class UserCreateForm(UserCreationForm):
#     email = forms.EmailField(required=True,label='Email',error_messages={'exists': 'This Already Exists'})

#     class Meta:
#         model = User
#         fields = ('email','password1','password2')

#     #placeholder
#     def __init__(self, *args, **kwargs):
#         super(UserCreateForm, self).__init__(*args, **kwargs)

#         self.fields['email'].widget.attrs['placeholder'] = 'Email'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


#     def save(self, commit=True):            # defalt commit value true
#         user = super(UserCreateForm, self).save(commit=False)
#         '''it will return to the obj but not save in database.useful for custom process'''
#         user.email = self.cleaned_data['email']  # valid or not
#         if commit:
#             user.save()
#         return user

#     def clean_email(self):
#         if User.objects.filter(email=self.cleaned_data['email']).exists():
#             raise forms.ValidationError(self.fields['email'].error_messages['exists'])
#         return self.cleaned_data['email']


