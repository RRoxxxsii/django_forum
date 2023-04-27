from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from account.forms import RegistrationForm, UserEditForm, UserRestoreForm
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
def personal_profile_view(request):
    template_name = 'account/user/personal_profile.html'

    context = {
        'user': request.user,
        'followers': request.user.followers
    }

    return render(request, template_name, context=context)


@login_required(redirect_field_name='login')
def edit_details(request):
    """
    Do not forget about transactions
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        gender_select_data = user_form.get_tuples_from_genders()
        if user_form.is_valid():

            # data got by post request
            name_to_change = request.POST.get('user_name')
            gender = request.POST.get('gender')
            profile_information = request.POST.get('profile_information')
            mobile = request.POST.get('mobile')
            telegram = request.POST.get('telegram')
            image = user_form.cleaned_data['image']


            # Username before change attempt
            current_user_name = Author.objects.get(id=request.user.id)
            if Author.objects.filter(user_name=name_to_change).count() == 0 or str(name_to_change) == str(current_user_name):
                user = Author.objects.get(user_name=current_user_name)

                if gender:
                    user.gender = gender
                if profile_information:
                    user.profile_information = profile_information
                if name_to_change:
                    user.user_name = name_to_change
                if mobile:
                    user.mobile = mobile
                if telegram:
                    user.telegram_link = telegram
                if image:
                    user.profile_photo = image

                user.save()
                messages.success(request, 'Ваши данные были изменены!')

            else:
                messages.error(request, f'Пользователь с именем {name_to_change} уже существует, попробуйте что-то другое')

        else:
            print(user_form.errors)

    else:
        user_form = UserEditForm(instance=request.user)
        gender_select_data = user_form.get_tuples_from_genders()

    return render(request, 'account/user/edit_profile.html', {'user_form': user_form,
                                                              'gender_select_data': gender_select_data})


@login_required(redirect_field_name='login')
def delete_photo(request):
    if request.method == 'POST':

        user = Author.objects.get(id=request.user.id)
        user.profile_photo.delete()
        user.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('account:personal_profile'))


@login_required(redirect_field_name='login')
def delete_user(request):
    """
    Makes user's account is_active attribute to False, but not
    deleting the account from the database itself
    """
    user = Author.objects.get(user_name=request.user.user_name)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def enable_user(request):
    if request.method == 'POST':
        form = UserRestoreForm(request.POST)
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        try:
            user = Author.objects.get(email=email, user_name=user_name)
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/account_restore_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/user/account_enable_message.html')
        except ObjectDoesNotExist:
            user = None
            error = f'Пользователя с почтой {email} и именем {user_name} не существует'
            messages.error(request, error)

        if user:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')

    else:
        form = UserRestoreForm()
    return render(request, 'account/user/restore_account.html', {'user_form': form})




