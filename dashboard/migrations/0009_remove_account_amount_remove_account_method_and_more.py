# Generated by Django 4.0 on 2022-01-04 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dashboard', '0008_paymentmethod_slug_alter_paymentmethod_api_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='account',
            name='method',
        ),
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('trans_ref', models.CharField(blank=True, max_length=225, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
