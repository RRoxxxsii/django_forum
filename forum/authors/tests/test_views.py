from django.test import TestCase, Client
from django.urls import reverse

from account.models import Author


class AuthorListView(TestCase):
    fixtures = ['fixtures.json']

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
    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        self.authors = Author.objects.all().exclude(id=1)

    def test_detail_view_response(self):
        for author in self.authors:
            response = self.client.get(reverse('authors:author_detail_view', kwargs={'pk': author.pk}))
            self.assertEqual(response.status_code, 200)


class FollowOtherProfileView(TestCase):

    """
    Test class to test changes and dynamic data on profile pages
    of other users.
    """

    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        self.user1 = Author.objects.get(id=1)
        self.user2 = Author.objects.get(id=10)
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')
        self.url = reverse('authors:author_detail_view', kwargs={'pk': self.user2.id})

    def test_follow_amount(self):
        self.client.post(self.url)
        self.assertEqual(len(self.user1.followers.all()), 1)
        self.assertEqual(len(self.user2.following.all()), 1)

    def test_author_list_view_when_user_does_not_follow_the_author(self):
        """
        Tests template button whether it is 'Подписаться' or 'Отписаться'
        and if amount of followers is displayed correctly
        """
        response = self.client.get(self.url)   # get method to get the page and not to press the follow button

        self.assertContains(response, 'Подписчики</a>: 0')  # zero followers
        self.assertContains(response, 'Подписаться')

        post_response = self.client.post(self.url)

    def test_template_user_is_followed(self):
        self.client.post(self.url) # response to press the button
        response = self.client.get(self.url)   # response to view changes
        self.assertContains(response, 'Подписчики</a>: 1')  # one follower
        self.assertContains(response, 'Отписаться')

    def test_unfollow_amount(self):
        self.client.post(self.url)      # follow to the author
        self.client.post(self.url)      # unfollow the author

        self.assertEqual(len(self.user1.followers.all()), 0)
        self.assertEqual(len(self.user2.following.all()), 0)

    def test_template_user_unfollow(self):
        self.client.post(self.url)  # follow to the author
        self.client.post(self.url)  # unfollow the author

        response = self.client.get(self.url)  # response to view changes
        self.assertContains(response, 'Подписчики</a>: 0')  # zero followers
        self.assertContains(response, 'Подписаться')

    def test_personal_profile_followers_and_following(self):
        self.client.post(self.url)
        response = self.client.get(reverse('account:personal_profile'))


class FollowersFollowingPersonalProfileView(TestCase):
    """
    Test class to test changes and dynamic data on your personal profile page.
    Especially check followers and following.
    """
    fixtures = ['fixtures.json']


    def setUp(self) -> None:
        self.user1 = Author.objects.get(id=1)
        self.user2 = Author.objects.get(id=10)
        self.url = reverse('authors:author_detail_view', kwargs={'pk': self.user2.id})
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')

    def test_following_amount_on_personal_profile_page(self):
        self.client.post(self.url)
        response = self.client.get(reverse('account:personal_profile'))    # follow another author
        self.assertContains(response, 'Подписки</a>: 1')
        self.assertContains(response, 'Подписчики</a>: 0')

    def test_followers_list_view(self):
        self.client.post(self.url)               # login to a user and make request to become a follower

        self.client.login(email='bronya@gmail.com', password='1234')
        response = self.client.get(reverse('authors:followers_list_view',
                                           kwargs={'pk': self.user2.pk}))  # go to user that is followed by the previous

        self.assertContains(response,
                            '/authors/1">RRoxxxsii')  # Check whether the user that follows is in the list of followers

        self.assertContains(response, 'Список подписчиков')        # Check if it is the list of followers

    def test_following_list_view(self):
        self.client.post(self.url)                # login to a user and make request to become a follower

        response = self.client.get(reverse('authors:following_list_view',
                                           kwargs={
                                               'pk': self.user1.pk}))  # go to current user profile and list of followings

        self.assertContains(response, '/authors/10">bronya')    # test if current user has the list of people he follows
        self.assertContains(response, 'Список подписок')

    def test_user_go_to_his_page_not_as_others_profile_but_as_his_page(self):
        """
        Test template fo a user when he clicks at his nickname to go to personal profile
        and finally goes to his personal profile with the address 'account/personal_profile',
        not the address 'author_detail_view'
        """
        self.client.post(self.url)
        response = self.client.get(reverse('authors:author_detail_view', kwargs={'pk': self.user1.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/personal_profile/')


class FollowUserNotAuthenticated(TestCase):
    fixtures = ['fixtures.json']


    def setUp(self) -> None:
        self.user1 = Author.objects.get(id=1)
        self.user2 = Author.objects.get(id=10)
        self.url = reverse('authors:author_detail_view', kwargs={'pk': self.user2.id})

    def test_follow_when_user_is_undefined(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, '/account/login/?next=/authors/10')



