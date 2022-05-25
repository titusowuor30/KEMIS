# Generated by Django 3.2.5 on 2022-05-25 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managemenet', '0013_auto_20220525_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste_invoice',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='waste_invoice',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=100),
        ),
    ]
