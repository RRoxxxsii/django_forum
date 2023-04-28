from django.views.generic import ListView


class AuthorFollowingFollowersListMixin(ListView):
    paginate_by = 20
    template_name = 'authors/authors_list_view.html'
    context_object_name = 'authors'

