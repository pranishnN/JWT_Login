# Generated by Django 5.0 on 2023-12-10 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masuser',
            name='email_id',
            field=models.CharField(error_messages={'unique': 'This email already exists'}, max_length=200, unique=True),
        ),
    ]
