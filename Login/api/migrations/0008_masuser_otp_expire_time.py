# Generated by Django 5.0 on 2023-12-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_masuser_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='masuser',
            name='otp_expire_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]