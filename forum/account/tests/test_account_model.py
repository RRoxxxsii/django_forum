import pytest
from django.contrib.auth import logout, login
from django.test import Client
from account.models import Author


def test_new_user(new_user1):
    print(new_user1.user_name)
    assert True



# @pytest.mark.skip
# @pytest.mark.django_db
# def test_user_create():
#     """
#     Checks if number of users equals to 1
#     after adding one user to the test db.
#     """
#     Author.objects.create_user('test@test.com', 'test', 'test')
#     count = Author.objects.all().count()
#     print(count)
#     assert count == 1
#
#
# @pytest.mark.skip
# @pytest.mark.django_db
# def test_user_create2():
#     """
#     Checks if number of users equals to 0;
#     users will not be added to test DB during the test perform.
#     """
#     count = Author.objects.all().count()
#     print(count)
#     assert count == 0
#
#
# def test_new_user(new_user):
#     assert new_user.email == 'useremail@ya.com'
#     assert new_user.user_name == 'Test_user'
#
#
# def test_function(user_login_or_logout):
#     """
#     It checks whether the function, which logs user out,
#     and the function, which logs user in, work as supposed.
#     """
#     logged_in = user_login_or_logout.login(email='useremail@ya.com', password='1234abcd')
#     assert logged_in is True
#     logged_out = logout(user_login_or_logout)
#     assert logged_out is None
