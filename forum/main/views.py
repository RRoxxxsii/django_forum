from django.db.models import Max
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from main.models import BlogCategory, SubCategory, Post


def pageNotFound(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response


class HomePageView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = BlogCategory.objects.all()
        context['title'] = 'Главная'
        context['categories'] = categories
        return context


def category_detail(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)               # Category
    subcategories = SubCategory.objects.filter(category=category.id)

    context = {'category': category, 'subcategories': subcategories, 'title': category}
    return render(request, 'main/category.html', context=context)


def subcategory_post(request, subcategory_slug):
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
    posts = Post.objects.filter(category=subcategory.id)
    context = {'posts': posts, 'title': subcategory}
    return render(request, 'main/posts.html', context=context)

