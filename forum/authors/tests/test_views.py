from django.test import TestCase, Client
from django.urls import reverse

from account.models import Author
from authors.factories.author import AuthorFactory


class AuthorListView(TestCase):
    fixtures = ['db.json']

    def setUp(self) -> None:
        self.users_amount = Author.objects.all().count()

    def test_list_view_response(self):
        response = self.client.get(reverse('authors:author_list_view'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_content(self):
        response = self.client.get(reverse('authors:author_list_view'))
        users_amount_listed = response.content.decode().count('<td class="list_item">') / 4    # Num of columns = 4
        self.assertEqual(users_amount_listed, self.users_amount)


class AuthorDetailView(TestCase):
    fixtures = ['db.json']

    def setUp(self) -> None:
        self.authors = Author.objects.all()

    def test_detail_view_response(self):
        for author in self.authors:
            response = self.client.get(reverse('authors:author_detail_view', kwargs={'pk': author.pk}))
            self.assertEqual(response.status_code, 200)







