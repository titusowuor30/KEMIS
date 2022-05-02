from django import forms
from .models import *

class add_company(forms.ModelForm):
        name = forms.CharField(label='Industry Name', required=True,widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Industry Name'}))
        email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@example.com'}))
        tel = forms.CharField(label='Email', required=True, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+254743793901','pattern':"^[+254]\d{10,13}$"}))
        website=forms.URLField(required=False, widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'example.com'}))
        description = forms.CharField(max_length=500,required=False,widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Company Intro'}))
        city = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City'}))
        location = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Location within city e.g along Maseno-Busia Road'}))
        
        
        class Meta:
            model=Industry
            fields=('name','description','email','tel','website','city','location')