import pytest

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



