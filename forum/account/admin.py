from django.contrib import admin
from account.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_active')
    ordering = ('is_superuser', 'is_staff', 'user_name', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active')




