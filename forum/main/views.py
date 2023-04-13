from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView


def pageNotFound(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response


class HomePageView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context



