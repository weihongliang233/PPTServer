from django.db import models

# Create your models here.


class User(models.Model):
    userID = models.CharField(default="000000000000", max_length=20)
    Name = models.CharField(default="hhh", max_length=20)
    School = models.CharField(default="No-School", max_length=20)
    Group = models.CharField(default="0", max_length=20)
    password = models.CharField(default="000000000000", max_length=20)
    filename = models.CharField(default="No-File-name", max_length=20)
    Identity = models.CharField(default="Student", max_length=20)
