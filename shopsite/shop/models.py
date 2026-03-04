from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


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
    image = models.ImageField(upload_to='products/', verbose_name="Фото товара")
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

class Cart(models.Model):
    # Один пользователь — одна корзина
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