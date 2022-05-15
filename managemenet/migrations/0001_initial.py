# Generated by Django 3.2.7 on 2022-05-14 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Inputs',
                'db_table': 'inputs',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WasteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('reusable', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('reuse_plan', models.CharField(choices=[('Donate', 'Donate'), ('Sell', 'Sell')], default='Donate', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/wastes/%Y-%m-%d')),
            ],
            options={
                'verbose_name_plural': 'Waste Products',
                'db_table': 'waste_products',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
                ('email', models.EmailField(default='company@example.com', max_length=100)),
                ('website', models.URLField(blank=True, max_length=500, null=True)),
                ('tel', models.CharField(blank=True, max_length=15, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('inputs', models.ManyToManyField(to='managemenet.Input')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='industries', to=settings.AUTH_USER_MODEL)),
                ('wasteproducts', models.ManyToManyField(to='managemenet.WasteProduct')),
            ],
            options={
                'verbose_name_plural': 'Industries',
                'db_table': 'industries',
                'ordering': ['-date_joined'],
            },
        ),
    ]
