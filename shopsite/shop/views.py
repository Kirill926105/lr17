from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Producer, Cart, CartItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import openpyxl
from io import BytesIO
from django.core.mail import EmailMessage
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Category, Producer, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer, ProducerSerializer, ProductSerializer,
    CartSerializer, CartItemSerializer,
    OrderSerializer, OrderItemSerializer
)
import random
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

def index(request):
    products = list(Product.objects.order_by('-id')[:12])
    popular = random.sample(products, min(6, len(products)))
    return render(request, 'shop/index.html', {'popular': popular})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    producers = Producer.objects.all()

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    producer = request.GET.get('producer', '')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category:
        products = products.filter(category_id=category)
    if producer:
        products = products.filter(producer_id=producer)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/catalog.html', {
        'page_obj': page_obj,
        'categories': categories,
        'producers': producers,
        'q': q,
        'category': category,
        'producer': producer,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    new_qty = int(request.POST.get('quantity', 1))
    if 0 < new_qty <= item.product.stock:
        item.quantity = new_qty
        item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if request.method == 'POST':
        target_email = request.POST.get('user_email')
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Товар', 'Количество', 'Цена за шт.', 'Итого'])
        for item in items:
            ws.append([item.product.name, item.quantity, item.product.price, item.get_cost()])
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        email = EmailMessage(
            'Ваш чек заказа',
            'Спасибо! Чек во вложении.',
            'krzkerouzz@gmail.com',
            [target_email],
        )
        email.attach('receipt.xlsx', buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.send()

        items.delete() 
        return render(request, 'shop/success.html', {'email': target_email})

    return render(request, 'shop/checkout.html', {'cart': cart})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Product.objects.all().select_related("category", "producer")

        q = self.request.query_params.get('q')
        category = self.request.query_params.get('category')
        producer = self.request.query_params.get('producer')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category_id=category)
        if producer:
            qs = qs.filter(producer_id=producer)

        return qs

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if Cart.objects.filter(user=self.request.user).exists():
            raise ValidationError("У пользователя уже есть корзина.")
        serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related("product", "cart")

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart:
            raise ValidationError("Сначала создайте корзину (Cart).")
        serializer.save(cart=cart)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user).select_related("product", "order")

    def perform_create(self, serializer):
        order = serializer.validated_data["order"]
        product = serializer.validated_data["product"]

        if order.user != self.request.user:
            raise ValidationError("Нельзя добавлять элементы в чужой заказ.")

        serializer.save(price=product.price)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_cart_add(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    if not product_id:
        return Response({'error': 'product_id is required'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity
    item.save()

    return Response({'ok': True, 'item_id': item.id, 'quantity': item.quantity})