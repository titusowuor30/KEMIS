# Generated by Django 3.2.7 on 2022-05-14 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managemenet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteproduct',
            name='reuse_plan',
            field=models.CharField(choices=[('Donate', 'Donate'), ('Sell', 'Sell'), ('Safe Dump', 'Safe Dump'), ('Reuse', 'Reuse')], default='Donate', max_length=20),
        ),
    ]
