from django.db.models import Max
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from account.models import Author
from main.forms import AddCommentForm
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

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            print(request)
            user = request.user
            text = request.POST.get('text')
            title = request.POST.get('title')
            subcategory_id = SubCategory.objects.get(slug=subcategory_slug).id
            context = {'posts': posts, 'title': subcategory, 'form': form, 'user_name': user_name}
            Post.objects.create(author=user, text=text, title=title, category_id=subcategory_id)

    else:
        form = AddCommentForm()

    if request.user.is_authenticated:
        user_name = Author.objects.get(user_name=request.user.user_name)
        context = {'posts': posts, 'title': subcategory, 'form': form, 'user_name': user_name}
    else:
        context = {'posts': posts, 'title': subcategory, 'form': form}
    return render(request, 'main/posts.html', context=context)





