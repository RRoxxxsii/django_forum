from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main:home')