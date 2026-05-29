from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Producer, Product, Cart, CartItem, Order, OrderItem, Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    producer_name = serializers.CharField(source="producer.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ("cart",)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ("user",)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ("price",)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("user",)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    favorite_category_name = serializers.CharField(
        source="favorite_category.name", read_only=True, default=""
    )

    class Meta:
        model = Profile
        fields = ("id", "username", "email", "role", "full_name", "phone", "address",
                  "favorite_category_id", "favorite_category_name", "delivery_city")
        read_only_fields = ("role",)

    favorite_category_id = serializers.IntegerField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        fav_cat_id = validated_data.pop("favorite_category_id", None)
        if fav_cat_id is not None:
            try:
                instance.favorite_category = Category.objects.get(id=fav_cat_id)
            except Category.DoesNotExist:
                instance.favorite_category = None
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"]
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=4)