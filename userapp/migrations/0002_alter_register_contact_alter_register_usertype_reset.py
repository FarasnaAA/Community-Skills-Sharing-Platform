# Generated by Django 5.1.5 on 2025-02-03 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='contact',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='usertype',
            field=models.CharField(default='admin', max_length=50),
        ),
        migrations.CreateModel(
            name='Reset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6, null=True)),
                ('otp_created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
