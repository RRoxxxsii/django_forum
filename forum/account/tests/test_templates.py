from django.test import Client, TestCase
from account.models import Author

fixtures = [
    'account/fixtures/mydata.json',
]

c = Client()


def test_login_template_response():
    """
    Checking response status code to login page
    """
    response_1 = c.get('/account/login/')
    response_2 = c.get('/none/')
    print(response_1.status_code)
    print(response_2.status_code)
    assert response_1.status_code == 200
    assert response_2.status_code == 404

@django.test.d
def test_signup_template_response(db):
    """
    Checking response status code to signup page
    """
    response_1 = c.get('/account/register/')
    response_2 = c.get('account/reg')
    assert response_1.status_code == 200
    assert response_2.status_code == 404

