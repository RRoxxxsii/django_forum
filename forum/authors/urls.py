from django.urls import path
from . import views


app_name = 'authors'

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='author_list_view'),
    path('<int:pk>', views.AuthorDetailView.as_view(), name='author_detail_view')
]
