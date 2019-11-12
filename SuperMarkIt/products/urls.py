from django.urls import path, re_path
from . import views

app_name = "products"

urlpatterns = [
    path('main/', views.main_products, name="main"),
    path('categories/', views.categories, name="categories"),
    re_path(r'categories/(?P<category_slug>[-\w]+)/', views.filtered_products, name="filtered_products"),
]
