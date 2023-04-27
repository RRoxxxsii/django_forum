from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from account.models import Author


class AuthorListView(ListView):
    template_name = 'authors/authors_list_view.html'
    context_object_name = 'authors'
    paginate_by = 20
    extra_context = {'header': 'Список пользователей'}

    def get_queryset(self):
        current_user_id = self.request.user.id
        queryset = Author.objects.exclude(id=current_user_id)
        return queryset


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_detail_view.html'

    def get(self, request, *args, **kwargs):
        other_user = self.get_object()
        try:
            current_user = Author.objects.get(user_name=request.user.user_name)
            if current_user.id == other_user.id:
                return redirect('account:personal_profile')
        except AttributeError:
            pass
        return super().get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        other_user = self.get_object()
        current_user = Author.objects.get(user_name=request.user.user_name)
        following = other_user.following.all()
        if str(other_user.user_name) != str(current_user.user_name):
            if current_user in following:
                other_user.following.remove(current_user.id)
            else:
                other_user.following.add(current_user.id)
            other_user.save()
            current_user.save()

        return redirect(request.META['HTTP_REFERER'])


class AuthorFollowersListView(ListView):
    paginate_by = 20
    template_name = 'authors/authors_list_view.html'
    context_object_name = 'authors'
    extra_context = {'header': 'Список подписчиков'}

    def get_queryset(self):
        user_obj = Author.objects.get(id=int(str(self.request).split('/')[-1].strip("'>")))
        queryset = user_obj.following.all()
        return queryset


class AuthorFollowingListView(ListView):
    paginate_by = 20
    template_name = 'authors/authors_list_view.html'
    context_object_name = 'authors'
    extra_context = {'header': 'Список подписок'}

    def get_queryset(self):
        user_obj = self.request.user
        queryset = user_obj.followers.all()
        return queryset



