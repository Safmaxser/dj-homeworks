# Generated by Django 4.2.13 on 2024-06-07 06:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisements', '0002_alter_advertisement_status_featuredads_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='favourite_by',
            field=models.ManyToManyField(related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FeaturedAds',
        ),
    ]