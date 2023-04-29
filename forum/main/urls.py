from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('category/posts/<slug:subcategory_slug>/', views.subcategory_post, name='subcategory_post'),
    path('category/posts/delete/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('category/posts/update/<int:pk>', views.PostUpdateView.as_view(), name='edit_post'),
    path('feedback/', views.FeedBackView.as_view(), name='feedback')

]

