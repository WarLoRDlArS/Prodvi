# Generated by Django 5.1.1 on 2024-10-12 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_users_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
