from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView

from account.forms import RegistrationForm, UserEditForm
from .models import Author
from .tokens import account_activation_token


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main:home')


def account_register(request):

    if request.user.is_authenticated:
        return redirect("main:home")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/register_email_confirm.html", {"form": registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Author.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("main:home")
    else:
        return render(request, "account/activation_invalid.html")


@login_required(redirect_field_name='login')
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        name_to_change = request.POST.get('first_name')
        current_user_name = Author.objects.get(user_name=request.user.user_name)
        if user_form.is_valid():
            if Author.objects.filter(user_name=name_to_change).count() == 0:

                user = Author.objects.get(user_name=current_user_name)
                user.user_name = name_to_change
                user.save()
                messages.success(request, f'Your name has been changed to {name_to_change}')

            else:
                messages.error(request, f'User with name {name_to_change} already exists, try something else')

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/edit_details.html', {'user_form': user_form})


@login_required(redirect_field_name='login')
def personal_profile_view(request):
    template_name = 'account/user/personal_profile.html'

    context = {
        'user': request.user,
    }

    return render(request, template_name, context=context)
