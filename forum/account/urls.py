from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from account.forms import UserLoginForm

app_name = 'account'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(template_name='account/login.html',
                                             form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),

    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.account_activate, name='activate'),
]

