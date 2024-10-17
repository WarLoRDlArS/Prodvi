# Generated by Django 5.0.2 on 2024-10-17 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_formassignedbyto_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilledForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filled_date', models.DateField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.employee')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.forms')),
            ],
        ),
    ]