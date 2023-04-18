from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from account.forms import UserLoginForm

app_name = 'account'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(template_name='account/login.html',
                                             form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),

    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.account_activate, name='activate'),
    path('personal_profile/', views.personal_profile_view, name='personal_profile'),
    path('personal_profile/edit_details/', views.edit_details, name='edit_details'),
    path('personal_profile/delete_photo/', views.delete_photo, name='delete_photo'),
    path('personal_profile/delete_user/', views.delete_user, name='delete_user'),
    path('personal_profile/delete_confirm/', TemplateView.as_view(template_name="account/user/delete_confirm.html"),
         name='delete_confirmation'),

]

