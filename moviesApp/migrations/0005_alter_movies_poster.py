# Generated by Django 5.1.7 on 2025-04-01 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesApp', '0004_alter_movies_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
