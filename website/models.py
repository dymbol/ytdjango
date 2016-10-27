#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class YT_URL(models.Model):
    url = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    status = models.DecimalField(decimal_places=0, max_digits=1)
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now=True)
    #1 - nieprzetworzony/w kolejce
    #2 - przetwarzany
    #3 - przetworzony
    #4 - błąd
    description = models.CharField(max_length=224)	
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.url

    class Meta:
        #sortowanie elementów po nazwie
        ordering = ['filename']
