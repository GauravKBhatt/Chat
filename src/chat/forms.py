from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'password',)
        
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role',)
        
        
        
        
        
        
        
        
        
        
    # widgets = {
    #         'email': forms.TextInput(attrs={
    #             'class': 'w-full py-4 px-6 rounded-xl border'
    #         }),
    #         'name': forms.TextInput(attrs={
    #             'class': 'w-full py-4 px-6 rounded-xl border'
    #         }),
    #         'role': forms.Select(attrs={
    #             'class': 'w-full py-4 px-6 rounded-xl border'
    #         })
    #     }