from django.test import Client, TestCase
from django.urls import reverse

from account.models import Author


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
        self.c = Client()
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
                                        {'user_name': 'RRoxxxsii', 'profile_information': 'Something cool',
                                         'telegram': 'https://t.me/mishkapiska', 'mobile': '88005553535'})

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_information, 'Something cool')
        self.assertEqual(self.user.telegram_link, 'https://t.me/mishkapiska')
        self.assertEqual(self.user.mobile, '88005553535')

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


