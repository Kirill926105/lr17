from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import connection
from shop.models import Category, Order, OrderItem, Producer, Product, Cart, CartItem, Profile

PRODUCERS = [
    {"name": "Meeple House", "country": "Польша", "description": "Польский бренд аксессуаров для настольных игр. Высокое качество и доступные цены."},
    {"name": "DiceForge", "country": "Беларусь", "description": "Минский производитель игральных кубиков и дайсов премиум-класса."},
    {"name": "CardGuard", "country": "Германия", "description": "Немецкое качество протекторов и органайзеров для карточных игр."},
    {"name": "PlaymatPro", "country": "Беларусь", "description": "Брестская компания по производству игровых ковриков и полей."},
    {"name": "MiniatureWorld", "country": "Беларусь", "description": "Витебский производитель миниатюр и фигурок для настольных игр."},
]

CATEGORIES = [
    {"name": "Протекторы для карт", "description": "Чехлы и протекторы для защиты карт во время игры"},
    {"name": "Игральные кубики", "description": "Дайсы всех размеров: d4, d6, d8, d10, d12, d20 и наборы"},
    {"name": "Игровые коврики", "description": "Плейматы для карточных и настольных игр"},
    {"name": "Органайзеры и боксы", "description": "Вставки и боксы для хранения и сортировки компонентов"},
    {"name": "Миниатюры и фигурки", "description": "Раскрашенные миниатюры для RPG и варгеймов"},
    {"name": "Держатели для карт", "description": "Кардхолдеры для комфортной игры"},
    {"name": "Жетоны и фишки", "description": "Токены, маркеры и монеты для отслеживания состояний"},
    {"name": "Сумки и рюкзаки", "description": "Сумки для переноски настольных игр"},
    {"name": "Трекеры и таймеры", "description": "Устройства для отслеживания ходов и времени"},
    {"name": "Аксессуары для покера", "description": "Карты, фишки и прочее для покерных турниров"},
]

PRODUCTS = [
    {"name": "Протекторы стандарт 66x91 100шт", "cat_idx": 0, "prod_idx": 2, "price": 12.50, "stock": 45, "desc": "Прозрачные протекторы для стандартных карт 66x91 мм. Упаковка 100 штук."},
    {"name": "Протекторы премиум 66x91 50шт", "cat_idx": 0, "prod_idx": 2, "price": 10.00, "stock": 30, "desc": "Протекторы премиум-класса с матовой поверхностью. 50 штук в упаковке."},
    {"name": "Протекторы мини 45x68 100шт", "cat_idx": 0, "prod_idx": 0, "price": 9.50, "stock": 55, "desc": "Чехлы для карт формата мини 45x68 мм. 100 штук."},
    {"name": "Протекторы для колоды 100шт", "cat_idx": 0, "prod_idx": 0, "price": 11.00, "stock": 40, "desc": "Универсальные протекторы для стандартной колоды карт."},
    {"name": "Набор дайсов d6 10шт", "cat_idx": 1, "prod_idx": 1, "price": 8.50, "stock": 60, "desc": "Набор из 10 шестигранных кубиков d6. Разные цвета."},
    {"name": "Полный набор дайсов d4-d20 7шт", "cat_idx": 1, "prod_idx": 1, "price": 15.00, "stock": 35, "desc": "Стандартный набор из 7 дайсов: d4, d6, d8, 2xd10, d12, d20."},
    {"name": "Металлические кубики d20", "cat_idx": 1, "prod_idx": 1, "price": 22.00, "stock": 20, "desc": "Тяжёлый металлический дайс d20 с гравировкой. Латунь."},
    {"name": "Кубики d6 с закруглёнными углами 5шт", "cat_idx": 1, "prod_idx": 1, "price": 7.00, "stock": 70, "desc": "Кубики d6 с мягкими углами. Приятно катать."},
    {"name": "Игровой коврик 60x35 см", "cat_idx": 2, "prod_idx": 3, "price": 25.00, "stock": 25, "desc": "Стандартный плеймат для card games. Резиновая основа."},
    {"name": "Игровой коврик с полем 60x90 см", "cat_idx": 2, "prod_idx": 3, "price": 35.00, "stock": 15, "desc": "Плеймат с нарисованным полем для RPG. Двусторонний."},
    {"name": "Коврик-пазл 4 части", "cat_idx": 2, "prod_idx": 3, "price": 40.00, "stock": 10, "desc": "Складной коврик из 4 частей-пазлов. Удобно для транспортировки."},
    {"name": "Органайзер для карт 4 отсека", "cat_idx": 3, "prod_idx": 2, "price": 18.00, "stock": 30, "desc": "Деревянный бокс с 4 отсеками для хранения карт."},
    {"name": "Органайзер-вставка в коробку", "cat_idx": 3, "prod_idx": 2, "price": 14.00, "stock": 25, "desc": "Вставка для стандартной коробки игры. Упорядочивает компоненты."},
    {"name": "Бокс для карт с крышкой 800 карт", "cat_idx": 3, "prod_idx": 0, "price": 22.00, "stock": 20, "desc": "Большой бокс на 800 карт с замком-клипсой. Пластик."},
    {"name": "Фигурка эльфа-лучника", "cat_idx": 4, "prod_idx": 4, "price": 16.00, "stock": 12, "desc": "Раскрашенная миниатюра эльфа-лучника. Высота 30 мм."},
    {"name": "Фигурка гнома-воина", "cat_idx": 4, "prod_idx": 4, "price": 16.00, "stock": 14, "desc": "Раскрашенная миниатюра гнома-воина. Высота 28 мм."},
    {"name": "Фигурка дракона 50 мм", "cat_idx": 4, "prod_idx": 4, "price": 28.00, "stock": 8, "desc": "Большая миниатюра дракона для D&D. Раскрашена вручную."},
    {"name": "Набор фигурок: орки 4шт", "cat_idx": 4, "prod_idx": 4, "price": 24.00, "stock": 10, "desc": "Набор из 4 фигурок орков. Разные позы и оружие."},
    {"name": "Держатель для карт деревянный", "cat_idx": 5, "prod_idx": 0, "price": 9.00, "stock": 35, "desc": "Деревянный кардхолдер на 6 карт. Эргономичная ручка."},
    {"name": "Держатель для карт пластиковый 2шт", "cat_idx": 5, "prod_idx": 0, "price": 7.00, "stock": 50, "desc": "Пластиковые держатели для карт. Набор 2 штуки."},
    {"name": "Держатель для карт-подставка", "cat_idx": 5, "prod_idx": 0, "price": 12.00, "stock": 22, "desc": "Подставка-пирамидка для демонстрации карт на столе."},
    {"name": "Жетоны опыта 10шт", "cat_idx": 6, "prod_idx": 1, "price": 5.50, "stock": 60, "desc": "Набор жетонов опыта. Акрил, двухсторонние."},
    {"name": "Фишки для покера 25мм 50шт", "cat_idx": 6, "prod_idx": 1, "price": 20.00, "stock": 15, "desc": "Покерные фишки диаметром 25 мм. 50 штук в наборе."},
    {"name": "Маркеры состояний 6шт", "cat_idx": 6, "prod_idx": 1, "price": 6.00, "stock": 40, "desc": "Маркеры для отслеживания состояний: огонь, яд, сон и др."},
    {"name": "Сумка для настолок малая", "cat_idx": 7, "prod_idx": 3, "price": 30.00, "stock": 18, "desc": "Сумка на 1-2 коробки настольных игр. Ремень через плечо."},
    {"name": "Рюкзак для настолок 40л", "cat_idx": 7, "prod_idx": 3, "price": 55.00, "stock": 8, "desc": "Большой рюкзак на 40 литров. Отделения для 4 коробок."},
    {"name": "Сумка-тубус для коврика", "cat_idx": 7, "prod_idx": 3, "price": 18.00, "stock": 12, "desc": "Чехол-тубус для транспортировки игрового коврика."},
    {"name": "Трекер очков электронный", "cat_idx": 8, "prod_idx": 1, "price": 15.00, "stock": 10, "desc": "Цифровой трекер очков. Батарейка в комплекте."},
    {"name": "Песочные часы 3 мин", "cat_idx": 8, "prod_idx": 0, "price": 6.00, "stock": 30, "desc": "Песочные часы на 3 минуты. Деревянная рама."},
    {"name": "Таймер для ходов", "cat_idx": 8, "prod_idx": 1, "price": 20.00, "stock": 15, "desc": "Электронный таймер для ограничения ходов. Звуковой сигнал."},
    {"name": "Покерный набор 500 фишек", "cat_idx": 9, "prod_idx": 1, "price": 65.00, "stock": 5, "desc": "Полный покерный набор: 500 фишек, карты, дилер."},
    {"name": "Карты для покера 2 колоды", "cat_idx": 9, "prod_idx": 2, "price": 12.00, "stock": 25, "desc": "2 колоды карт для покера. Пластик, смываемые."},
    {"name": "Коврик для покера 180x90", "cat_idx": 9, "prod_idx": 3, "price": 45.00, "stock": 7, "desc": "Большой коврик для покерного стола. Зелёное сукно."},
    {"name": "Набор фишек для покера 200шт", "cat_idx": 9, "prod_idx": 1, "price": 30.00, "stock": 12, "desc": "Набор из 200 покерных фишек в кейсе."},
]

USERS_DATA = [
    {"username": "ivan_p", "password": "pass12345", "role": "CUSTOMER", "full_name": "Иван Петров", "phone": "+375291234567", "address": "ул. Ленина, 10, кв. 5", "city": "Минск"},
    {"username": "olga_s", "password": "pass12345", "role": "CUSTOMER", "full_name": "Ольга Смирнова", "phone": "+375331112233", "address": "пр-т Независимости, 55, кв. 12", "city": "Минск"},
    {"username": "dmitry_k", "password": "pass12345", "role": "CUSTOMER", "full_name": "Дмитрий Козлов", "phone": "+375257778899", "address": "ул. Московская, 25", "city": "Брест"},
    {"username": "elena_m", "password": "pass12345", "role": "MANAGER", "full_name": "Елена Морозова", "phone": "+375296665544", "address": "ул. Гагарина, 7, кв. 34", "city": "Гомель", "staff": True, "superuser": False},
    {"username": "admin_bg", "password": "admin12345", "role": "ADMIN", "full_name": "Артём Администратор", "phone": "+375447770011", "address": "пр-т Победителей, 1", "city": "Минск", "staff": True, "superuser": True},
]

CART_ITEMS = [
    {"user_idx": 0, "items": [(0, 2), (4, 1), (8, 1)]},
    {"user_idx": 1, "items": [(5, 3), (1, 2)]},
    {"user_idx": 2, "items": [(14, 1), (17, 1), (21, 4)]},
    {"user_idx": 3, "items": [(2, 5), (6, 1), (11, 1)]},
    {"user_idx": 4, "items": [(9, 2), (15, 1), (22, 3), (27, 1)]},
]


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными (категории, производители, товары, пользователи, корзины)"

    def handle(self, *args, **options):
        self._clear_data()
        producers = self._create_producers()
        categories = self._create_categories()
        products = self._create_products(categories, producers)
        users = self._create_users()
        self._create_carts(users, products)
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))

    def _clear_data(self):
        self.stdout.write("Очистка старых данных...")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Profile.objects.all().delete()
        user_names = [u["username"] for u in USERS_DATA]
        User.objects.filter(username__in=user_names).delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Producer.objects.all().delete()

        for table in ["shop_order", "shop_orderitem", "shop_producer", "shop_category", "shop_product", "shop_cartitem", "shop_cart", "auth_user", "shop_profile"]:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
            except Exception:
                pass

    def _create_producers(self):
        self.stdout.write("Создание производителей...")
        result = []
        for p in PRODUCERS:
            result.append(Producer.objects.create(**p))
        return result

    def _create_categories(self):
        self.stdout.write("Создание категорий...")
        result = []
        for c in CATEGORIES:
            result.append(Category.objects.create(**c))
        return result

    def _create_products(self, categories, producers):
        self.stdout.write("Создание товаров...")
        result = []
        for p in PRODUCTS:
            result.append(Product.objects.create(
                name=p["name"],
                description=p["desc"],
                price=p["price"],
                stock=p["stock"],
                category=categories[p["cat_idx"]],
                producer=producers[p["prod_idx"]],
            ))
        return result

    def _create_users(self):
        self.stdout.write("Создание пользователей...")
        result = []

        for u in USERS_DATA:
            user = User.objects.create_user(username=u["username"], password=u["password"])
            user.is_staff = u.get("staff", False)
            user.is_superuser = u.get("superuser", False)
            user.save()
            profile = Profile.objects.get(user=user)
            profile.role = u["role"]
            profile.full_name = u["full_name"]
            profile.phone = u["phone"]
            profile.address = u["address"]
            profile.delivery_city = u["city"]
            profile.save()
            result.append(user)
        return result

    def _create_carts(self, users, products):
        self.stdout.write("Создание корзин...")
        for ci in CART_ITEMS:
            cart = Cart.objects.create(user=users[ci["user_idx"]])
            for product_idx, quantity in ci["items"]:
                CartItem.objects.create(cart=cart, product=products[product_idx], quantity=quantity)
