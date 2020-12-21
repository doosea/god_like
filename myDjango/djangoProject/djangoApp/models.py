from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)

    class Meta:
        db_table = "t_movie"