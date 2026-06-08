from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Cart, CartItem, Category, Order, Producer, Product


class CatalogSearchTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Cards")
        producer = Producer.objects.create(name="Meeple Co", country="RU")
        Product.objects.create(
            name="Sleeves",
            description="Hidden keyword",
            image="",
            price=100,
            stock=5,
            category=category,
            producer=producer,
        )

    def test_catalog_search_uses_product_name_only(self):
        response = self.client.get(reverse("catalog"), {"q": "Hidden"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Товары не найдены")


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="sales@example.com",
)
class CheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="pass12345")
        category = Category.objects.create(name="Cards")
        producer = Producer.objects.create(name="Meeple Co", country="RU")
        self.product = Product.objects.create(
            name="Sleeves",
            description="Protect cards",
            image="",
            price=100,
            stock=5,
            category=category,
            producer=producer,
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_checkout_creates_order_sends_receipt_and_clears_cart(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("checkout"), {"user_email": "buyer@example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.get().quantity, 2)
        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["buyer@example.com"])
        self.assertEqual(len(mail.outbox[0].attachments), 1)
