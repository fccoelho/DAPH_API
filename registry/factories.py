import factory
from factory.django import DjangoModelFactory
from datetime import timezone

from .models import Article, Author, Manuscript

class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    address = ""

class ManuscriptFactory(DjangoModelFactory):
    class Meta:
        model = Manuscript

    title = factory.Faker('sentence')
    date_submission = factory.Faker('date_time_this_year', tzinfo=timezone.utc)
    file = factory.Faker('file_path', extension='pdf')

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.authors.add(author)

class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    manuscript = factory.SubFactory(ManuscriptFactory)
