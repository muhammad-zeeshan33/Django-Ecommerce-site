from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('shop/<int:p_id>', views.product, name='product'),
    path('categories/<int:category_id>', views.category, name='category')
]
