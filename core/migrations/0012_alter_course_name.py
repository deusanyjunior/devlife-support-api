# Generated by Django 3.2.6 on 2021-10-07 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_long_answer_answer_student_input'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
