from django.urls import path
from blog import views
app_name = 'blog'


urlpatterns = [
    path('', views.index, name='bolg_index'),
    path('<int:blog_id>', views.detail, name='blog_detail'),
    path('category/<int:category_id>', views.category, name='blog_category'),
    path('tag/<int:tag_id>', views.tags, name='blog_tags'),
    path('search/', views.search, name='blog_search'),
    path('sarchives/<year>/<month>', views.archives, name='blog_archives'),
]