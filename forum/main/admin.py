from django.contrib import admin
from main.models import BlogCategory, SubCategory, Post


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
    ordering = ('category_name', 'id')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('sub_category_name',)}
    list_filter = ('category', )
    list_ordering = ('sub_category_name', 'category')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('category', )
    search_fields = ('author', )


