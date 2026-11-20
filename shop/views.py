
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Product
from .cart import get_cart


def product_list(request):
    products = Product.objects.filter(
        is_available=True,
        stock__gt=0
    )

    return render(request, "shop/product_list.html", {
        "products": products
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart = request.session.get("shopping_cart", {})

    key = str(product.id)
    current_quantity = int(cart.get(key, 0))

    if current_quantity < product.stock:
        cart[key] = current_quantity + 1
        request.session["shopping_cart"] = cart

        messages.success(
            request,
            f"{product.name} added to cart!"
        )
    else:
        messages.error(
            request,
            "Available stock limit reached."
        )

    return redirect("shop:product_list")


def cart_detail(request):
    items, total = get_cart(request)

    return render(request, "shop/cart_detail.html", {
        "items": items,
        "total": total
    })


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("shopping_cart", {})

    key = str(product.id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity.")
        return redirect("shop:cart_detail")

    if quantity <= 0:
        cart.pop(key, None)

    elif product.is_available and quantity <= product.stock:
        cart[key] = quantity

    else:
        messages.error(
            request,
            "Requested quantity exceeds available stock."
        )

    request.session["shopping_cart"] = cart

    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = request.session.get("shopping_cart", {})

    cart.pop(str(product_id), None)

    request.session["shopping_cart"] = cart

    messages.success(request, "Product removed from cart.")

    return redirect("shop:cart_detail")
