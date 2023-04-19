from account.models import Author
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BlogCategory(models.Model):
    """
    This model describes a category name
    """

    category_name = models.CharField(max_length=255, unique=True)
    category_slug = models.SlugField(max_length=255, unique=True)
    category_photo = models.ImageField(blank=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ('category_name', )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(BlogCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("main:post_detail", args=[self.slug])

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sub_category_name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.sub_category_name

    class Meta:
        verbose_name = _('Подкатегория')
        verbose_name_plural = _('Подкатегории')
        ordering = ('-sub_category_name', )


class Post(models.Model):
    """
    To create a detailed link to each post it is necessary to indicate a slug firstly
    and secondly an ID of a post:
    .../where-to-go/1/...
    It is important in case if there are several articles with one name
    """

    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.SET(_('Удаленный аккаунт')))
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.title_slug:
            self.title = slugify(f"{self.title}-{self.pk}-")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ('-created_at', 'author')

