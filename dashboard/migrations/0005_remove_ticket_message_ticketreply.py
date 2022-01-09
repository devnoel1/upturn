# Generated by Django 4.0 on 2021-12-30 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dashboard', '0004_alter_account_amount_alter_orders_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='message',
        ),
        migrations.CreateModel(
            name='TicketReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]