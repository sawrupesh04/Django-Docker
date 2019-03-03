from django.db import models


class Patient(models.Model):
    p_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    start = models.CharField(max_length=200)
    weight = models.FloatField()
    height = models.FloatField()
    time_stamp = models.DateTimeField()
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    email_id = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    occupation = models.CharField(max_length=200)

    def __str__(self):
        return self.name
