# Generated by Django 3.2.6 on 2021-10-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_news_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, upload_to='avatars/', verbose_name='Заставка'),
        ),
    ]
