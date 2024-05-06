from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.IntegerField(primary_key=True, )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=1)
    image = models.CharField(max_length=200, null=True)
    release_date = models.CharField(max_length=10)
    lte_exists = models.BooleanField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Phone, self).save(*args, **kwargs)
