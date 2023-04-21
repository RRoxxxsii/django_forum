from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('category/posts/<slug:subcategory_slug>/', views.subcategory_post, name='subcategory_post'),

]

