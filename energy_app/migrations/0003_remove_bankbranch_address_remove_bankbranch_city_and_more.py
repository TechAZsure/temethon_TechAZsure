# Generated by Django 5.1.6 on 2025-02-08 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy_app', '0002_remove_bankbranch_is_active_bankbranch_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankbranch',
            name='address',
        ),
        migrations.RemoveField(
            model_name='bankbranch',
            name='city',
        ),
        migrations.RemoveField(
            model_name='bankbranch',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='bankbranch',
            name='state',
        ),
        migrations.AlterField(
            model_name='bankbranch',
            name='bank_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankbranch',
            name='branch_code',
            field=models.CharField(default=0, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankbranch',
            name='contact_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='bankbranch',
            name='email',
            field=models.EmailField(default=0, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankbranch',
            name='manager_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bankbranch',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
