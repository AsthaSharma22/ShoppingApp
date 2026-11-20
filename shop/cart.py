
from .models import Product


def get_cart_count(request):
    cart = request.session.get("shopping_cart", {})
    return sum(int(quantity) for quantity in cart.values())


def get_cart(request):
    cart_data = request.session.get("shopping_cart", {})

    products = Product.objects.filter(
        id__in=cart_data.keys(),
        is_available=True
    )

    items = []
    total = 0

    for product in products:
        quantity = int(cart_data[str(product.id)])

        # Do not display quantities greater than available stock
        quantity = min(quantity, product.stock)

        if quantity <= 0:
            continue

        line_total = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total
        })

        total += line_total

    return items, total
