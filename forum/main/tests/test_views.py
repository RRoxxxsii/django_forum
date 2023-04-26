from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from main.models import BlogCategory, SubCategory, Post


class MainViews(TestCase):

    fixtures = ['db.json']

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

        for post in self.posts:
            self.assertContains(response, post.author)
            self.assertContains(response, post)


class ViewFormAddComment(TestCase):

    fixtures = ['db.json']

    def setUp(self) -> None:
        self.posts = Post.objects.filter(category=2)         # posts for one specific category
        self.subcategory = SubCategory.objects.get(id=2)

    def test_posts(self):
        post_amount = len(self.posts)
        self.assertEqual(post_amount, 2)

    def test_post_page_when_user_is_not_authenticated(self):
        """
        When user is not logged in he sees the
        link 'Войдите в систему прежде чем оставлять комментарии'.
        """
        response = self.client.get(reverse('main:subcategory_post', kwargs={'subcategory_slug': self.subcategory.slug}))
        self.assertContains(response, 'Войдите в систему прежде чем оставлять комментарии')

    def test_post_page_when_user_is_authenticated(self):
        """
        When user is logged in he sees the
        button 'Оставить комментарий'.
        """
        self.client.login(email='mishabur38@gmail.com', password='1234')
        response = self.client.get(reverse('main:subcategory_post', kwargs={'subcategory_slug': self.subcategory.slug}))
        self.assertContains(response, 'Оставить комментарий')

    def test_add_post(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')

        response = self.client.post(reverse('main:subcategory_post',
                                            kwargs={'subcategory_slug': self.subcategory.slug}),
                                    {'title': 'Не знаю как',
                                     'text': 'Подскажите, как писать оптимальный код на Python?'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.posts), 3)


class ViewEditPost(TestCase):

    fixtures = ['db.json']

    def setUp(self) -> None:
        # POST BY SUPERUSER
        self.post = Post.objects.get(id=3)
        self.url = reverse('main:edit_post', kwargs={'pk': self.post.id})
        self.data = {
            'title': 'Changed the content of the post',
            'text': 'Changed the text of the post LOL XD'
        }

    def test_edit_post_if_user_is_not_authenticated(self):
        print(self.post, self.post.author)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_edit_post_if_user_is_authenticated(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')

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
    fixtures = ['db.json']

    def setUp(self) -> None:
        # POST BY SUPERUSER
        self.post = Post.objects.get(id=3)
        self.url = reverse('main:delete_post', kwargs={'pk': self.post.id})

    def test_delete_post_if_user_is_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_if_user_is_authenticated(self):
        self.client.login(email='mishabur38@gmail.com', password='1234')

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




