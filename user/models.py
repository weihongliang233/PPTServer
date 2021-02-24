from django.db import models

# Create your models here.


class User(models.Model):
    #userID = models.CharField(default="000000000000",max_length=20)
    #Name = models.CharField(default="No-Name",max_length=20)
    School = models.CharField(default="No-School",max_length=20)
    Group = models.IntegerField(default=0)
    password = models.CharField(default="000000000000",max_length=20)
    filename=models.CharField(default="No-File-name",max_length=20)
    Identity=models.CharField(default="No-Identiy",max_length=20)
