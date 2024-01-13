from django.db import models


class Reservation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    reservation_number = models.CharField(max_length=6)
    reservation_date = models.DateTimeField()
