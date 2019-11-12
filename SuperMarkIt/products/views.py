from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def filtered_products(request, category_slug):
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    print(category, products)
    template = "products/categories/filter.html"
    context = {"categories": categories, "product_query_set": products, "category": category}
    return render(request, template, context)


def main_products(request):
    products = Product.objects.all()
    return render(request, "products/main_products.html", {"products": products})


def categories(request):
    categories = Category.objects.all()
    return render(request, "products/categories.html", {"categories": categories})
