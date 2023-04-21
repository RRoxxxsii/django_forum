from django.test import TestCase, Client
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
