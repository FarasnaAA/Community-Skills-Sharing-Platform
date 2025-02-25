# Generated by Django 5.1.5 on 2025-02-19 06:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0011_register_followers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(choices=[('Tech', 'Technology'), ('Art', 'Arts'), ('Music', 'Music'), ('Cooking', 'Cooking'), ('Fitness', 'Fitness'), ('Other', 'Other')], max_length=100, null=True)),
                ('sub_category', models.CharField(max_length=100, null=True)),
                ('skill_created_at', models.DateTimeField(auto_now_add=True)),
                ('skill_video', models.FileField(blank=True, null=True, upload_to='skill_videos/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
