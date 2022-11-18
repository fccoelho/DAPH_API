from ctypes import addressof
from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Reviewer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class WalletAddress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=100)

class Manuscript(models.Model):
    title = models.CharField(max_length=200)
    date_submission = models.DateTimeField('Date Submission')
    authors = models.ManyToManyField(Author)
    file = models.FileField(verbose_name='Manuscript file')

class Review(models.Model):
    reviewer_id = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    manuscript_id = models.ForeignKey(Manuscript, on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Review file')
    status = models.CharField(max_length=50, choices = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    date_submission = models.DateTimeField('Date Submission', auto_now_add=True)
    
class Article(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE)