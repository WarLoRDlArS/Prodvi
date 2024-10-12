# Generated by Django 5.1.1 on 2024-10-12 04:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('deptid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Forms',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('review_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('fresh', 'Fresh'), ('finished', 'Finished')], max_length=20)),
                ('submission_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('empid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('empname', models.CharField(max_length=255)),
                ('is_manager', models.BooleanField(default=False)),
                ('empdept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('managerid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('is_manager', models.BooleanField(default=True)),
                ('user_pid', models.CharField(max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FormAssignedByTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_date', models.DateField()),
                ('has_filled', models.BooleanField(default=False)),
                ('has_viewed', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.employee')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.forms')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.manager')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='managerid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.manager'),
        ),
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.manager'),
        ),
        migrations.CreateModel(
            name='QuestionAnswers',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False)),
                ('answer_text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NumericResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_value', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.questionanswers')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('question_type', models.CharField(choices=[('numeric', 'Numeric'), ('text', 'Text')], max_length=10)),
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.forms')),
            ],
        ),
        migrations.AddField(
            model_name='questionanswers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.questions'),
        ),
    ]
