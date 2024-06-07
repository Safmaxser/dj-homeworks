from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    DRAFT = "DRAFT", "Черновик"
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.DRAFT
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    favourite_by = models.ManyToManyField(User, blank=True,
                                          related_name='favourites',
                                          through='FeaturedAds')


class FeaturedAds(models.Model):
    ads = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                            related_name='favourites_lines')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favourites_lines')
