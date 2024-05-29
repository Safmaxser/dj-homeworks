from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='measurements')
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', max_length=None, null=True,
                              blank=True)
