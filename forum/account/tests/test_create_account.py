from django.test import Client
from django.test import TestCase

from account.models import Author


class TestUserSignUp(TestCase):

    fixtures = [
        'db.json'
        ]

    def test_create_new_user(self):
        """
        Tests custom function for user creating
        """
        users_before_creating_new_user = Author.objects.all()
        user_amount_before_creating_new_user = users_before_creating_new_user.count()

        new_user = Author.objects.create_user('brother@gmail.com', 'brother', '1234')

        users_after_creating_new_user = Author.objects.all()
        user_amount_after_creating_new_user = users_after_creating_new_user.count()

        assert user_amount_before_creating_new_user + 1 == user_amount_after_creating_new_user

    def test_change_user_status_where_user_is_active_equals_false(self):
        """
        Change user is_active status to False
        """
        user_last = Author.objects.get(pk=1)
        user_last.is_active = False
        assert user_last.is_active is False


