# Generated by Django 5.1.1 on 2024-10-13 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_forms_review_date_alter_forms_submission_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forms',
            name='review_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forms',
            name='submission_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]