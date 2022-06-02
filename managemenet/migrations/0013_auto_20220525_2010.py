# Generated by Django 3.2.5 on 2022-05-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managemenet', '0012_auto_20220525_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste_invoice',
            name='message',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='waste_invoice',
            name='payment_method',
            field=models.CharField(default='Mpesa', max_length=50),
        ),
    ]