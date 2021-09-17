from django.urls import path

from . import views
urlpatterns = [
    path('',views.blogs, name='blogs'),
    path('comments',views.comment, name='comment'),
    path('<int:blog_id>',views.blog, name='blog'),
]