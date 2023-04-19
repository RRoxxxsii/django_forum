import re

from django.test import Client, TestCase
from django.urls import reverse

from account.models import Author
from django.core import mail


class TestAccountView(TestCase):
    fixtures = ['data.json']

    def setUp(self) -> None:
        self.c = Client()
        self.user = Author.objects.get(id=1)

    def test_account_views_when_user_is_undefined(self):
        """
        Tests if undefined user have access to pages not only available to all user, but unavailable
        to not authenticated users.
        """

        login_view_resp = self.c.get(reverse('account:login'))
        register_view_resp = self.c.get(reverse('account:register'))
        personal_profile_resp = self.c.get(reverse('account:personal_profile'))
        edit_details_resp = self.c.get(reverse('account:edit_details'))

        assert login_view_resp.status_code == 200
        assert register_view_resp.status_code == 200
        assert personal_profile_resp.status_code == 302
        assert edit_details_resp.status_code == 302

    def test_account_views_when_user_is_not_undefined(self):
        """
        If authenticated user has access to login required page.
        """
        self.c.login(email='mishabur38@gmail.com', password='1234')

        personal_profile_resp = self.c.get(reverse('account:personal_profile'))
        edit_details_resp = self.c.get(reverse('account:edit_details'))

        assert personal_profile_resp.status_code == 200
        assert edit_details_resp.status_code == 200


class UserEditTest(TestCase):

    fixtures = ['mydata.json']

    def setUp(self):
        self.user = Author.objects.get(user_name='RRoxxxsii')

    def test_user_redirected_if_not_logged_in(self):
        request_data = self.client.post('/account/personal_profile/edit_details/', {'user_name': 'RRoxxxsii'})
        assert request_data.status_code == 302

    def test_user_information_before_change(self):
        self.assertEqual(self.user.profile_information, 'Python backend developer')
        self.assertEqual(self.user.profile_photo, 'photos/2023/04/16/lera-2024.jpg')
        self.assertEqual(self.user.telegram_link, 'https://t.me/RRoxxxsii')
        self.assertEqual(self.user.mobile, '89086469507')

    def test_user_edit_form_with_correct_data(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')
        self.client.post('/account/personal_profile/edit_details/',
                                        {'user_name': 'fakename', 'profile_information': 'Something cool',
                                         'telegram': 'https://t.me/mishkapiska', 'mobile': '88005553535'})

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_information, 'Something cool')
        self.assertEqual(self.user.telegram_link, 'https://t.me/mishkapiska')
        self.assertEqual(self.user.mobile, '88005553535')
        self.assertEqual(self.user.user_name, 'fakename')

    def test_change_details_that_cannot_be_changed(self):
        """
        Trying to change such detail as username,
        but under conditions when this data is already
        stored in the DataBase. If username already exists
        and owned by another user, it won't be updated for
        current user according to function logic. Relevant
        name for the field is always unique or current for
        the accessing the form.
        __________________________________________________

        If details except username were changed and the
        username that already owned by another user was
        changed as well, it means that there is a error
        in the view; it is not correct function
        behaviour.
        """

        def response_request(name: str) -> str:
            self.client.login(email='mishabur38@gmail.com', password='1234')
            self.client.post('/account/personal_profile/edit_details/',
                             {'user_name': name, 'profile_information': 'Something cool'})
            self.user.refresh_from_db()
            return self.user.profile_information

        self.assertEqual(response_request('homer'), 'Python backend developer')   # Name exists
        self.assertEqual(response_request('RRoxxxsii'), 'Something cool')         # Name owned by current user
        self.assertEqual(response_request('fakename'), 'Something cool')          # Name does not exist, so free to use


class UserDeletePhoto(TestCase):

    fixtures = ['mydata.json']

    def setUp(self) -> None:
        self.user = Author.objects.get(user_name='RRoxxxsii')

    def test_send_delete_request(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')

        request = self.client.post('/account/personal_profile/delete_photo')
        self.assertEqual(request.status_code, 301)


class UserDeleteAccount(TestCase):

    fixtures = ['mydata.json']

    def setUp(self) -> None:
        self.user = Author.objects.get(user_name='RRoxxxsii')

    def test_make_account_inactive(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')
        self.assertEqual(self.user.is_active, True)

        request = self.client.get(reverse('account:delete_user'))
        self.user.refresh_from_db()

        self.assertEqual(request.status_code, 302)
        self.assertEqual(self.user.is_active, False)


class UserRestoreAccount(TestCase):

    fixtures = ['mydata.json']

    def setUp(self) -> None:
        self.user = Author.objects.get(user_name='RRoxxxsii')

    def test_restore_account_with_correct_data(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')
        self.client.get(reverse('account:delete_user'))
        self.user.refresh_from_db()

        # tests if user not active to request email message later
        self.assertEqual(self.user.is_active, False)

        # correct data for the current user
        self.client.post(reverse('account:restore'), {'email': 'mishabur38@gmail.com', 'user_name': 'RRoxxxsii'})

        # check if email message exists, and it's subject is as excpected
        email_sent = mail.outbox
        self.assertEqual(len(email_sent), 1)
        self.assertEqual(email_sent[0].subject, 'Activate your account')

        # test that user is not active yet
        self.assertEqual(self.user.is_active, False)

        # get link form email and test it
        link = re.search(r'http://.+', email_sent[0].body).group()
        response = self.client.get(link)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()

        # test if user active
        self.assertEqual(self.user.is_active, True)

    def test_restore_account_with_incorrect_data(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')
        self.client.get(reverse('account:delete_user'))
        self.user.refresh_from_db()

        # tests if user not active to request email message later
        self.assertEqual(self.user.is_active, False)

        # send post request with incorrect data
        self.client.post(reverse('account:restore'), {'email': 'incorrect@gmail.com', 'user_name': 'incorrect'})

        email_sent = mail.outbox
        self.assertEqual(len(email_sent), 0)

