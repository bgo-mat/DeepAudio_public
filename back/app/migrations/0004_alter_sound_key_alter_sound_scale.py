# Generated by Django 5.1.3 on 2024-11-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_user_favorite_packs_user_favorite_sounds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sound',
            name='key',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sound',
            name='scale',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
