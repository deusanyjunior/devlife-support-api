# Generated by Django 3.2.6 on 2022-02-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_offering_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='allow_submissions',
            field=models.BooleanField(default=True),
        ),
    ]