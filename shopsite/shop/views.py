from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Producer, Cart, CartItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import openpyxl
from io import BytesIO
from django.core.mail import EmailMessage

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    producers = Producer.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    cat_id = request.GET.get('category')
    prod_id = request.GET.get('producer')
    if cat_id:
        products = products.filter(category_id=cat_id)
    if prod_id:
        products = products.filter(producer_id=prod_id)

    return render(request, 'shop/product_list.html', {
        'products': products, 
        'categories': categories, 
        'producers': producers
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
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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