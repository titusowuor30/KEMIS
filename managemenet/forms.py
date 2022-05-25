from django import forms
from django.db.models import fields
from .models import *


class inputsForm(forms.ModelForm):
    name = forms.CharField(label='Input Title', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Waste Title'}))
    description = forms.CharField(max_length=500, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Short Input description'}))

    class Meta:
        model = Input
        fields = ("name", "description")


class addWasteForm(forms.ModelForm):
    name = forms.CharField(label='Waste Title', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Waste Title'}))
    price = forms.DecimalField(label='Price', required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Leave blank if you wish to donate waste', 'id': 'pricefield'}))
    description = forms.CharField(max_length=500, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Short waste description'}))
    image = forms.ImageField(label='Waste Title', required=False, widget=forms.FileInput(
        attrs={'class': 'form-control', 'placeholder': 'Upload Waste Image'}))

    class Meta:
        model = WasteProduct
        fields = ("name", "category", "description",
                  "reuse_plan", "price", "image")
        WASTE_CATEGORIES = (("", "Please Select Waste  Category"),
                            ("Solid Waste", "Solid Waste"),
                            ("Liquid Waste", "Liquid Waste"),
                            ("Reusable Waste", "Reusable Waste"),
                            ("Hazardous Waste", "Hazardous Waste"))
        RECYCLE_PLANS = (("Donate", "Donate"), (
            "Sell", "Sell"), ("Safe Dump", "Safe Dump"), ("Reuse", "Reuse"))
        widgets = {
            'category': forms.Select(choices=WASTE_CATEGORIES, attrs={'class': 'form-control'}),
            'reuse_plan': forms.Select(choices=RECYCLE_PLANS, attrs={'id': 'reuseplan', 'class': 'form-control d-block'}),
        }


class add_company(forms.ModelForm):
    name = forms.CharField(label='Industry Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Industry Name'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'example@example.com'}))
    tel = forms.CharField(label='Email', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '+254743793901', 'pattern': "^[+254]\d{10,13}$"}))
    website = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'example.com'}))
    description = forms.CharField(max_length=500, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Company Intro'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City'}))
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Location within city e.g along Maseno-Busia Road'}))

    class Meta:
        model = Industry
        fields = ('name', 'description', 'email',
                  'tel', 'website', 'city', 'location')
