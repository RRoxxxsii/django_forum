from django.shortcuts import render
from django.views.generic import ListView

from account.models import Author


class AuthorListView(ListView):
    template_name = 'authors/authors_list_view.html'
    queryset = Author.objects.all()
    context_object_name = 'authors'
    paginate_by = 20

