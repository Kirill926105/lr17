from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'producers', views.ProducerViewSet, basename='producers')
router.register(r'carts', views.CartViewSet, basename='carts')
router.register(r'cart-items', views.CartItemViewSet, basename='cart-items')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'order-items', views.OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.product_list, name='catalog'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout_view, name='checkout'),

    path('api/cart/add/', views.api_cart_add, name='api_cart_add'),

    path('api/', include(router.urls)),
]