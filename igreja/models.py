from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.title} ------- {self.artist}'


class Played(models.Model):
    music = models.ForeignKey(Music, on_delete=models.DO_NOTHING)
    tone = models.CharField(max_length=2)
    position = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f'{self.music.title} ------- {self.date}'
