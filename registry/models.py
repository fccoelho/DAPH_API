from ctypes import addressof
from typing_extensions import Required
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='First Name')
    last_name = models.CharField(max_length=128, verbose_name='Last Name')
    email = models.EmailField()
    address = models.CharField(max_length=256)


class Manuscript(models.Model):
    title = models.CharField(max_length=200)
    date_submission = models.DateTimeField('Date Submission', auto_now_add=True)
    authors = models.ManyToManyField(Author)
    file = models.FileField(verbose_name='Manuscript file')


class Article(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE)
