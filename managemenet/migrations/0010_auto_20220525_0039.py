# Generated by Django 3.2.5 on 2022-05-24 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managemenet', '0009_wasteproduct_mass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteproduct',
            name='mass',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wasteproduct',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
