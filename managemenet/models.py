from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Input(models.Model):
    name=models.CharField(max_length=200,unique=True)
    description=models.TextField(max_length=255,blank=True,null=True)

    class Meta:
        db_table='inputs'
        verbose_name_plural='Inputs'
        ordering = ['name']

    def __str__(self):
        return self.name 
    
class WasteProduct(models.Model):
     name=models.CharField(max_length=200,unique=True)
     date_added=models.DateTimeField(auto_now_add=True,blank=True,null=True)
     description=models.TextField(max_length=255,blank=True,null=True)
     reusable=models.BooleanField(default=False)
     status=models.BooleanField(default=False)
     reuse_plan=models.CharField(default="Donate",max_length=20,choices=(("Donate","Donate"),("Sell","Sell"),("Safe Dump","Safe Dump"),("Reuse","Reuse")),verbose_name="Recyle Plan")
     price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
     image=models.ImageField(upload_to="media/wastes/%Y-%m-%d",blank=True,null=True)
     
     class Meta:
            db_table='waste_products'
            verbose_name_plural='Waste Products'
            ordering = ['-date_added']

     def __str__(self):
        return self.name 
          
        
class Industry(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='industries')
    name=models.CharField(max_length=100,unique=True)
    date_joined=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    email=models.EmailField(max_length=100,default="company@example.com")
    website=models.URLField(max_length=500,blank=True,null=True)
    tel=models.CharField(max_length=15,blank=True,null=True)
    description=models.TextField(max_length=255,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    inputs=models.ManyToManyField(Input)
    wasteproducts=models.ManyToManyField(WasteProduct)

    class Meta:
        db_table='industries'
        verbose_name_plural='Industries'
        ordering = ['-date_joined']

    def __str__(self):
        return self.name   
