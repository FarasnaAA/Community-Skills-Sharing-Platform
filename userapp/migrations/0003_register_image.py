# Generated by Django 5.1.5 on 2025-02-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_alter_register_contact_alter_register_usertype_reset'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
