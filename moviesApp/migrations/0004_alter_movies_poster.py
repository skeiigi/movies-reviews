# Generated by Django 5.1.7 on 2025-04-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesApp', '0003_alter_movies_about_alter_movies_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='poster',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
