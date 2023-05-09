from account.models import Author
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BlogCategory(models.Model):
    """
    This model describes a category name
    """

    category_name = models.CharField(max_length=255, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Слаг категории')
    category_photo = models.ImageField(blank=True, verbose_name='Изображение категории')

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ('category_name', )

    def get_absolute_url(self):
        return reverse("main:category", args=[self.slug])

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='Внешний ключ категории')
    sub_category_name = models.CharField(max_length=255, verbose_name='Название подкатегории')
    slug = models.SlugField(max_length=255, verbose_name='Слаг подкатегории')

    def __str__(self):
        return self.sub_category_name

    class Meta:
        verbose_name = _('Подкатегория')
        verbose_name_plural = _('Подкатегории')
        ordering = ('-sub_category_name', )

    def get_absolute_url(self):
        return reverse("main:subcategory_post",  args=[self.slug])


class Post(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Внешний ключ подкатегории')
    author = models.ForeignKey(Author, on_delete=models.SET(_('Удаленный аккаунт')), verbose_name='Внешний ключ автора')
    title = models.CharField(max_length=255, verbose_name='Заголовок поста')
    text = models.TextField(verbose_name='Пост')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации поста')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время редактирования')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован', help_text='Опубликован ли пост')

    def get_absolute_url(self):
        return reverse('main:edit_post', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ('-created_at', 'author')


class FeedBack(models.Model):

    text = models.TextField(verbose_name='Текст обратной связи')

    def __str__(self):
        return self.text

