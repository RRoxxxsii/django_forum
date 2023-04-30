from captcha.fields import CaptchaField
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings
from django.urls import reverse

from account.models import Author
from main.models import BlogCategory, SubCategory, Post
from captcha.conf import settings as captcha_settings


class MainViews(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        self.categories = BlogCategory.objects.all()          # All categories
        self.category = BlogCategory.objects.get(pk=2)        # One category
        self.subcategories = SubCategory.objects.filter(category__pk=2)
        self.subcategory = SubCategory.objects.get(id=2)
        self.posts = Post.objects.filter(category__pk=2)

    def test_index_page_view(self):
        """
        If dynamic data from the index page exists and displayed correctly
        and request status code to the index page = 200.
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.category_name)
        self.assertContains(response, self.category.category_photo)

    def test_subcategory_page_view(self):
        """
        Tests if response status code to category page = 200
        and subcategories are displayed correctly.
        """
        for category in self.categories:
            response = self.client.get(reverse('main:category', kwargs={'slug': category.slug}))
            self.assertEqual(response.status_code, 200)

        response_category_where_pk_equals_two = self.client.get(reverse('main:category',
                                                                        kwargs={'slug': self.category.slug}))
        for subcategory in self.subcategories:
            self.assertContains(response_category_where_pk_equals_two, subcategory)

    def test_post_page_view(self):
        """
        Tests if response status code to post page = 200
        and posts and their authors are displayed correctly.
        """
        response = self.client.get(reverse('main:subcategory_post', kwargs={'subcategory_slug': self.subcategory.slug}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.posts[0].author)
        self.assertContains(response, self.posts[0])


class ViewFormAddComment(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        self.posts = Post.objects.filter(category=2)         # posts for one specific category
        self.subcategory = SubCategory.objects.get(id=2)

    def test_post_page_when_user_is_not_authenticated(self):
        """
        When user is not logged in he sees the
        link 'Войдите в систему прежде чем оставлять комментарии'.
        """
        response = self.client.get(reverse('main:subcategory_post', kwargs={'subcategory_slug': self.subcategory.slug}))
        self.assertContains(response, '<h4>Войдите в систему прежде чем оставлять комментарии</h4>')

    def test_post_page_when_user_is_authenticated(self):
        """
        When user is logged in he sees the
        button 'Оставить комментарий'.
        """
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')
        response = self.client.get(reverse('main:subcategory_post', kwargs={'subcategory_slug': self.subcategory.slug}))
        self.assertContains(response, 'Оставить комментарий')

    def test_add_post(self):
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')
        response = self.client.post(reverse('main:subcategory_post',
                                            kwargs={'subcategory_slug': self.subcategory.slug}),
                                    {'title': 'Не знаю как',
                                     'text': 'Подскажите, как писать оптимальный код на Python?'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.posts), 15)


class ViewEditPost(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        # POST BY SUPERUSER
        self.post = Post.objects.get(id=54)
        self.url = reverse('main:edit_post', kwargs={'pk': self.post.id})
        self.data = {
            'title': 'Changed the content of the post',
            'text': 'Changed the text of the post LOL XD'
        }

    def test_edit_post_if_user_is_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_edit_post_if_user_is_authenticated(self):
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')

        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()

        self.assertEqual(self.post.title, 'Changed the content of the post')
        self.assertEqual(self.post.text, 'Changed the text of the post LOL XD')

    def test_edit_if_user_goes_to_post_owned_by_another_author(self):
        self.client.login(email='misha@yandex.ru', password='1234')

        response = self.client.post(self.url, self.data)

        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, 'Changed the content of the post')
        self.assertNotEqual(self.post.text, 'Changed the text of the post LOL XD')

        self.assertEqual(response.status_code, 404)


class ViewDeletePost(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        # POST BY SUPERUSER
        self.post = Post.objects.get(id=54)
        self.url = reverse('main:delete_post', kwargs={'pk': self.post.id})

    def test_delete_post_if_user_is_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_if_user_is_authenticated(self):
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        try:
            self.post.refresh_from_db()
        except ObjectDoesNotExist:
            assert True

    def test_delete_if_user_goes_to_post_owned_by_another_author(self):
        self.client.login(email='misha@yandex.ru', password='1234')

        response = self.client.post(self.url)

        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 404)


class FeedBackFormView(TestCase):

    fixtures = ['fixtures.json']

    def setUp(self) -> None:
        self.user1 = Author.objects.get(id=1)
        self.client.login(email='mishabur38@gmail.com', password='pro191Ji321')
        try:
            captcha_settings.CAPTCHA_TEST_MODE = True
            self.response = self.client.post(reverse('main:feedback'),
                                             data={'text': 'Сообщение на почту админу', "captcha_0": "PASSED",
                                                   "captcha_1": "PASSED"})
            self.email = mail.outbox
        finally:
            captcha_settings.CAPTCHA_TEST_MODE = False

    def test_email_from_the_form_delivered(self):
        self.assertEqual(len(self.email), 1)

    def test_email_sender(self):
        self.assertEqual(self.email[0].from_email, 'root@localhost')

    def test_email_content(self):
        assert 'Сообщение на почту админу' in self.email[0].body
        assert 'mishabur38@gmail.com' in self.email[0].body
