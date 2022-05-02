from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Input(models.Model):
    name=models.CharField(max_length=200,unique=True)
    description=models.TextField(max_length=255,blank=True,null=True)

    class Meta:
        verbose_name_plural='Inputs'
        ordering = ['name']

    def __str__(self):
        return self.name 
    
class WasteProduct(models.Model):
     name=models.CharField(max_length=200,unique=True)
     description=models.TextField(max_length=255,blank=True,null=True)
     
     class Meta:
            verbose_name_plural='Waste Products'
            ordering = ['name']

     def __str__(self):
        return self.name 
          
        
class Industry(models.Model):
    name=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,default="company@example.com")
    website=models.URLField(max_length=500,blank=True,null=True)
    tel=models.CharField(max_length=15,blank=True,null=True)
    description=models.TextField(max_length=255,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    inputs=models.ManyToManyField(Input)
    wasteproducts=models.ManyToManyField(WasteProduct)

    class Meta:
        verbose_name_plural='Industries'
        ordering = ['name']

    def __str__(self):
        return self.name   
