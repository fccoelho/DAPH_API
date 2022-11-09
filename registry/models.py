from ctypes import addressof
from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_reviewer = models.BooleanField(default=False)

class WalletAddress(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null = True)
    wallet_address = models.CharField(max_length=100)

class Manuscript(models.Model):
    title = models.CharField(max_length=200)
    date_submission = models.DateTimeField('Date Submission', auto_now_add = True)
    authors = models.ManyToManyField(Author)
    file = models.FileField(verbose_name='Manuscript file')

class Review(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, null = True)
    manuscript_id = models.ForeignKey(Manuscript, on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Review file')
    status = models.CharField(max_length=50, choices = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    date_submission = models.DateTimeField('Date Submission', auto_now_add = True)
    number_votes = models.IntegerField(default=0)
    sum_votes = models.FloatField(default=0)

class Article(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE)