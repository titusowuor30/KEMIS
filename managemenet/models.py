from django.db import models
from django.contrib.auth.models import User
# Create your models here.


WASTE_CATEGORIES = (("Solid Waste", "Solid Waste"),
                    ("Liquid Waste", "Liquid Waste"),
                    ("Reusable Waste", "Reusable Waste"),
                    ("Hazardous Waste", "Hazardous Waste"))


class Input(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'inputs'
        verbose_name_plural = 'Inputs'
        ordering = ['name']

    def __str__(self):
        return self.name


class WasteProduct(models.Model):
    category = models.CharField(max_length=100,
                                choices=WASTE_CATEGORIES, default="Solid Waste")
    name = models.CharField(max_length=200, unique=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    available = models.BooleanField(default=True)
    reuse_plan = models.CharField(default="Donate", max_length=20, choices=(("Donate", "Donate"), (
        "Sell", "Sell"), ("Safe Dump", "Safe Dump"), ("Reuse", "Reuse")), verbose_name="Recyle Plan")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    image = models.ImageField(
        upload_to="media/wastes/%Y-%m-%d", blank=True, null=True)

    class Meta:
        db_table = 'waste_products'
        verbose_name_plural = 'Waste Products'
        ordering = ['-date_added']

    def __str__(self):
        return self.name


class Industry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='industries')
    name = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    email = models.EmailField(max_length=100, default="company@example.com")
    website = models.URLField(max_length=500, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    inputs = models.ManyToManyField(Input)
    wasteproducts = models.ManyToManyField(WasteProduct)

    class Meta:
        db_table = 'industries'
        verbose_name_plural = 'Industries'
        ordering = ['-date_joined']

    def __str__(self):
        return self.name


class waste_invoice(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wastes_invoice', blank=True, null=True)
    invoice_id = models.CharField(max_length=100, default="#INV001")
    companyA = models.ForeignKey(
        Industry, on_delete=models.CASCADE, related_name='waste_invoices')
    companyB = models.ForeignKey(Industry, on_delete=models.CASCADE)
    waste = models.ForeignKey(
        WasteProduct, on_delete=models.CASCADE, related_name='wastes', blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transportation = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, default="Mpesa")
    message = models.TextField(max_length=1500, blank=True, null=True)
    status = models.CharField(max_length=100, choices=(
        ("Paid", "Paid"), ("Rejected", "Rejected"), ("Pending", "Pending")), default="Pending")
    delivered = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoices'
        verbose_name_plural = 'invoices'
        ordering = ['-date']

    def __str__(self):
        return self.invoice_id

    @ property
    def get_total_amount(self):
        total = 0
        total += self.transportation + self.amount
        return total
