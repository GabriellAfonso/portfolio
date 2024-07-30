from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, blank=True)


class Played(models.Model):
    music = models.ForeignKey(Music)
    tone = models.CharField(max_length=2)
    position = models.IntegerField()
    date = models.DateField()
