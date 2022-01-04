# Generated by Django 3.2.6 on 2021-12-22 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_exercise_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='type',
            field=models.CharField(choices=[('CODE', 'Code'), ('QUIZ', 'Quiz'), ('TEXT', 'Text'), ('CSS', 'CSS'), ('SELF', 'Self-assess')], max_length=4),
        ),
    ]
