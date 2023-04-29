from django.urls import path
from . import views


app_name = 'authors'

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='author_list_view'),
    path('<int:pk>', views.AuthorDetailView.as_view(), name='author_detail_view'),
    path('followers/<int:pk>', views.AuthorFollowersListView.as_view(), name='followers_list_view'),
    path('following/<int:pk>', views.AuthorFollowingListView.as_view(), name='following_list_view'),
    path('filter_by_followers/', views.AuthorFilterByFollowersAmount.as_view(), name='author_filter_by_followers')
]

