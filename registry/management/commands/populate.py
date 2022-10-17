import random

from django.core.management.base import BaseCommand
from django.db import transaction

from registry.factories import ArticleFactory, AuthorFactory, ManuscriptFactory
from registry.models import Article, Author, Manuscript

import factory

NUM_AUTHORS = 10
NUM_MANUSCRIPTS = 100
NUM_ARTICLES = 50

class Command(BaseCommand):
    help = 'Populate the database with some initial data'

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Author, Manuscript, Article]
        for model in models:
            model.objects.all().delete()

        authors = AuthorFactory.create_batch(NUM_AUTHORS)

        manuscripts = []

        for _ in range(NUM_MANUSCRIPTS):
            authors_sample = random.sample(authors, random.randint(1, 3))
            manuscript = ManuscriptFactory(authors=authors_sample)
            manuscripts.append(manuscript)

        for i in range(NUM_ARTICLES):
            manuscript = manuscripts[i]
            ArticleFactory(manuscript=manuscript)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
