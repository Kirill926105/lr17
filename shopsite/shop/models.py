from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

class Producer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название (Бренд)")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(upload_to='products/', verbose_name="Фото товара", blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)], 
        verbose_name="Цена"
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name="Количество на складе"
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, verbose_name="Производитель")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        constraints = [
            models.CheckConstraint(condition=models.Q(stock__gte=0), name="stock_non_negative"),
        ]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Корзина пользователя: {self.user.username}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def get_cost(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("paid", "Оплачен"),
        ("sent", "Отправлен"),
        ("done", "Завершен"),
        ("canceled", "Отменен"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")

    def __str__(self):
        return f"Заказ #{self.id} ({self.user.username})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"


class Profile(models.Model):
    ROLE_CHOICES = [
        ("CUSTOMER", "Покупатель"),
        ("MANAGER", "Менеджер"),
        ("ADMIN", "Администратор"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CUSTOMER", verbose_name="Роль")
    full_name = models.CharField(max_length=150, blank=True, verbose_name="Полное имя")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес доставки")

    favorite_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Любимая категория"
    )
    delivery_city = models.CharField(max_length=100, blank=True, verbose_name="Город доставки")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()