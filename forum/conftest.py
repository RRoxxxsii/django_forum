import pytest
from django.contrib.auth import login, logout
from django.test import Client
from account.models import Author
from pytest_factoryboy import register
from tests.factory import AuthorFactory, SubCategoryFactory, PostFactory, BlogCategoryFactory


register(AuthorFactory)
register(SubCategoryFactory)
register(PostFactory)
register(BlogCategoryFactory)


@pytest.fixture()
def new_user1(db):
    user = Author.objects.create(email='bro@yandex.ru', user_name='somebody', password='1234')
    return user





#
#
# @pytest.fixture()
# def user_1(db):
#     user = Author.objects.create_user('test_user@gmail.com', 'test_user', 'test')
#     print(user)
#
#
# @pytest.fixture()
# def new_user_factory(db):
#     def create_app_user(username, email, password='1234abcd', is_active=True):
#         user = Author.objects.create_user(user_name=username, password=password,
#                                           email=email, is_active=is_active)
#
#         return user
#
#     return create_app_user
#
#
# @pytest.fixture
# def new_user(db, new_user_factory):
#     return new_user_factory('Test_user', 'useremail@ya.com')
#
#
# @pytest.fixture
# def new_user2(db, new_user_factory):
#     return new_user_factory('Test_user', 'useremail@ya.com')
#
#
# @pytest.fixture()
# def user_login_or_logout(db, new_user_factory):
#     client = Client(new_user_factory('Test_user', 'useremail@ya.com'))
#     return client
#




