import factory
from account.models import Author
from main.models import BlogCategory, SubCategory, Post
from faker import Faker


fake = Faker()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    user_name = 'Jonny Depp'


class BlogCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = BlogCategory

    category_name = 'django'
    category_slug = 'django'


class SubCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SubCategory

    category = factory.SubFactory(BlogCategoryFactory)
    sub_category_name = 'Django models'
    slug = 'django-models'


class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post

    category = factory.SubFactory(SubCategoryFactory)
    author = factory.SubFactory(AuthorFactory)
    title = 'Have a issue in django models'
    title_slug = 'have-a-issue-in-django-models'
    text = fake.text()

