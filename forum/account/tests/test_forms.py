import pytest
from account.forms import RegistrationForm, UserLoginForm

@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "12345a", "12345a", True),
        ("user1", "a@a.com", "12345a", "", False),
        ("user1", "a@a.com", "", "12345a", False),
        ("user1", "a@a.com", "12345a", "12345b", False),
        ("user1", "a@.com", "12345a", "12345a", False),
    ],
)
@pytest.mark.django_db
def test_create_account(user_name, email, password, password2, validity):
    form = RegistrationForm(
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert form.is_valid() is validity






