# Generated by Django 4.0 on 2022-01-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_transactions_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='amount',
            field=models.CharField(default=0.0, max_length=225),
        ),
    ]
