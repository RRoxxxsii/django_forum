from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from account.models import Author


class AuthorListView(ListView):
    template_name = 'authors/authors_list_view.html'
    context_object_name = 'authors'
    paginate_by = 20

    def get_queryset(self):
        current_user_id = self.request.user.id
        queryset = Author.objects.exclude(id=current_user_id)
        return queryset


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_detail_view.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        other_user = self.get_object()
        current_user = Author.objects.get(user_name=request.user.user_name)
        followers = other_user.followers.all()

        if str(other_user.user_name) != str(current_user.user_name):
            if current_user in followers:
                other_user.followers.remove(current_user.id)
            else:
                other_user.followers.add(current_user.id)
            other_user.save()
            current_user.save()

        return redirect(request.META['HTTP_REFERER'])




