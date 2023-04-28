# Generated by Django 4.2 on 2023-04-28 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_user_pic.png', null=True, upload_to='profile_images', verbose_name='Profile image'),
        ),
    ]
