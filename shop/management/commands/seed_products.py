
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):

    help = "Add sample products to the database"

    def handle(self, *args, **kwargs):

        products = [
            {
                "name": "Banana Chips",
                "description": "Crispy and tasty banana chips.",
                "price": 30.00,
                "stock": 20,
                "is_available": True,
            },
            {
                "name": "Misti Doi",
                "description": "A famous Bengali sweet made with curd, milk and jaggery.",
                "price": 45.00,
                "stock": 15,
                "is_available": True,
            },
            {
                "name": "Milk",
                "description": "Contains 500ml.",
                "price": 32.00,
                "stock": 25,
                "is_available": True,
            },
        ]

        for product in products:

            obj, created = Product.objects.get_or_create(
                name=product["name"],
                defaults=product
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{obj.name} added successfully!"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"{obj.name} already exists!"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Sample products processed!")
        )
