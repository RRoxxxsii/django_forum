import pytest
from django.test import Client
from account.forms import RegistrationForm


@pytest.mark.parametrize(
    'user_name, email, password, password2, validity',
    [
        ('user1', 'a@a.com', '12345a', '12345a', True),
        ('user1', 'a@a.com', '12345a', '1234', False),
        ('user1', 'a@a.com', '123', '1234', False),
        ('user1', 'a.com', '12345a', '1234', False),
        ('user1', 'a@a.com', '12345aa', '12345aa', True),

    ],
)
@pytest.mark.django_db
def test_create_account(client, user_name, email, password, password2, validity):
    form = RegistrationForm(
        data={
            'user_name': user_name,
            'email': email,
            'password': password,
            'password2': password2
        }
    )

    assert form.is_valid() is validity


c = Client()


# @pytest.mark.django_db
# def test_account_registration():
#     response_1 = c.post('/account/register/', {'user_name': 'maggy', 'email': 'mish@yanndex.ru',
#                                                'password': '1234', 'password2': '1234'})
#     response_2 = c.post('/account/register/', {'user_name': '', 'email': 'mish@yanndex.ru',
#                                                'password': '1234', 'password2': '1234'})
#     assert response_1.status_code == 200
#     assert response_2.status_code != 200


