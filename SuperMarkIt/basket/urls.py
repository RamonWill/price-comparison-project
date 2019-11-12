from django.urls import path, re_path
from . import views

app_name = "basket"

urlpatterns = [
    path('basket/', views.basket_view, name="basket"),
    re_path(r'(?P<slug>[\w-]+)/', views.update_basket, name="update")
]
