from django.db import models


class Puzzle(models.Model):
    url = models.URLField(max_length=100)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
