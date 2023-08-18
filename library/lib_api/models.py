from telnetlib import STATUS
from django.db import models

# Create your models here.

class Book(models.Model):

    name = models.TextField()
    author= models.TextField()
    status = models.TextField(default='AVAILABLE')
    borrowed_by = models.IntegerField(null=True)

    class Meta:
        db_table = 'books'
