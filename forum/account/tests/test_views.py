import pytest
from django.test import Client, TestCase
from django.urls import reverse

from account.models import Author
from conftest import new_user1


class TestAccountView(TestCase):

    fixtures = ['data.json']

    def setUp(self) -> None:
        self.c = Client()

    def test_account_views_when_user_is_undefined(self):
        """
        Tests if undefined user have access to pages not only available to all user, but unavailable
        to not authenticated users.
        """

        login_view = self.c.get(reverse('account:login'))
        register_view = self.c.get(reverse('account:register'))
        personal_profile = self.c.get(reverse('account:personal_profile'))

        assert login_view.status_code == 200
        assert register_view.status_code == 200
        assert personal_profile.status_code == 302

    def test_account_views_when_user_is_not_undefined(self):
        """
        If authenticated user has access to login required page.
        """
        self.c.login(email='mishabur38@gmail.com', password='1234')
        personal_profile = self.c.get(reverse('account:personal_profile'))

        assert personal_profile.status_code == 200




