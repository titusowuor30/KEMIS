# Generated by Django 3.2.5 on 2022-05-24 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managemenet', '0010_auto_20220525_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wasteproduct',
            name='mass',
        ),
    ]