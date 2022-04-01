from django.db import models

# Create your models here.
class Industry(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=255)
    location=models.CharField(max_length=255)
    inputs=models.ForeignKey('Inputs',on_delete=models.CASCADE)
    waste_product=models.ForeignKey('WasteProducts',on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural='Industries'
    def __str__(self):
        return self.name   
    
class Inputs(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(max_length=255)
    
    class Meta:
        verbose_name_plural='Inputs'
    def __str__(self):
        return self.name 
    
class WasteProducts(models.Model):
     name=models.CharField(max_length=200)
     description=models.TextField(max_length=255)
     
     class Meta:
            verbose_name_plural='Waste Products'
     def __str__(self):
        return self.name 
          
        