from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from products.models import Product

from .models import Basket, BasketItem


def basket_view(request):
    try:
        session_id = request.session["basket_id"]
    except KeyError:
        session_id = None

    if session_id:
        basket = Basket.objects.get(id=session_id)
        context = {"basket": basket}
    else:
        empty_message = "Your basket is currently empty"
        context = {"empty": True, "empty_message": empty_message}

    # basket = Basket.objects.all()[0]
    template = "basket/basket-view.html"
    return render(request, template, context)


def update_basket(request, slug):
    # session expires after x seconds of inactivity
    request.session.set_expiry(1800)
    try:
        quantity = request.GET.get("quantity")
        update_quantity = True
    except ValueError:
        quantity = None
        update_quantity = False

    # Get if cart exists. if not create a new one.
    try:
        session_id = request.session["basket_id"]
    except KeyError:
        new_basket = Basket()
        new_basket.save()
        request.session["basket_id"] = new_basket.id
        session_id = new_basket.id

    basket = Basket.objects.get(id=session_id)

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass

    # the below returns ("Basket item object", "true/false")
    basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

    if created:
        print("yeah")
    else:
        pass

    if quantity and update_quantity:
        if int(quantity) <= 0:
            basket_item.delete()
        else:
            basket_item.quantity = quantity
            basket_item.save()
    else:
        pass

    # if basket_item not in basket.items.all():
    #     basket.items.add(basket_item)
    # else:
    #     basket.items.remove(basket_item)

    new_total = 0.00
    for item in basket.basketitem_set.all():
        total_product = float(item.product.price_sainsburys) * item.quantity
        new_total += total_product

    request.session["items_total"] = basket.basketitem_set.count()
    print(basket.basketitem_set.count())
    basket.total = new_total
    basket.save()
    return HttpResponseRedirect(reverse("basket:basket"))
