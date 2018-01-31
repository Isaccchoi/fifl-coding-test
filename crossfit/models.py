from django.db import models

from member.models import phone_regex


class Center(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=13)
