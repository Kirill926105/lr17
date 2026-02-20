from django.shortcuts import render

from django.http import HttpResponse

# 8c. Главная страница
def home_page(request):
    return HttpResponse("""
        <h1>Главная страница</h1>
        <p>Добро пожаловать!</p>
        <ul>
            <li><a href='/author/'>Об авторе</a></li>
            <li><a href='/store/'>О магазине</a></li>
        </ul>
    """)

# 8a. Страница об авторе
def author_page(request):
    return HttpResponse("<h1>Об авторе</h1><p>Работу выполнил: Кульбицкий Кирилл, студент группы 88ТП.</p><a href='/'>Назад</a>")

# 8b. Страница о магазине
def store_page(request):
    return HttpResponse("""
        <h1>Магазин:</h1>
        <br><a href='https://znaemigraem.by/catalog/accessories/?srsltid=AfmBOopaBqhdV51U_Y0-9o5FKuJ5fhPcGiZED3jeX3PseA1dB8i6lFLZ'>Аксессуары</a>
        <br><p>Протекторы Card-Pro - Perfect Fit USA std для карт Munchkin (100 шт.) 58x88 мм (CP001)
1 отзыв
5 р.
Наличие:
КУПИТЬ

Звёзды Акариоса. Плеймат
Новинка
Предзаказ
Звёзды Акариоса. Плеймат
155 р.
ПРЕДЗАКАЗ

Премиум альбом для карт 4x4 Alpha. Premium. Черный (CBPU16-BLACK)
Новинка
Премиум альбом для карт 4x4 Alpha. Premium. Черный (CBPU16-BLACK)
169.70 р.
Наличие:
КУПИТЬ

Протекторы для ККИ Alpha - CCG Size (Perfect Fit) 100 шт. (64х89 мм)
Новинка
Протекторы для ККИ Alpha - CCG Size (Perfect Fit) 100 шт. (64х89 мм)
6.70 р.
Наличие:
КУПИТЬ

Протекторы Card-Pro - PREMIUM Dixit Size (50 шт.) 82x123 мм (CP008P)
Протекторы Card-Pro - PREMIUM Dixit Size (50 шт.) 82x123 мм (CP008P)
6 р.
Наличие:
КУПИТЬ

Прозрачные протекторы Card-Pro PREMIUM Quadro Medium для настольных игр (50 шт.) 75x75 мм
Прозрачные протекторы Card-Pro PREMIUM Quadro Medium для настольных игр (50 шт.) 75x75 мм
5.50 р.
Наличие:
КУПИТЬ

Премиум альбом для карт 4x5 Alpha. Premium. Черный (CBPU20-BLACK)
Новинка
Премиум альбом для карт 4x5 Alpha. Premium. Черный (CBPU20-BLACK)
235 р.
Наличие:
КУПИТЬ

Прозрачные протекторы Card-Pro PREMIUM Euro для настольных игр (50 шт.) 59x92 мм
Прозрачные протекторы Card-Pro PREMIUM Euro для настольных игр (50 шт.) 59x92 мм
5.50 р.
Наличие:
КУПИТЬ

Протекторы Стандарт Pantheon Sleeves Standart Card Game Гермес 63.5x88 mm 110 шт. (SCG-001)
Протекторы Стандарт Pantheon Sleeves Standart Card Game Гермес 63.5x88 mm 110 шт. (SCG-001)
5.90 р.
Наличие:
КУПИТЬ

Покорение Марса. Большая коробка (BIG BOX)
Покорение Марса. Большая коробка (BIG BOX)
1-5
120-180
12+ лет
420.90 р.
Наличие:
КУПИТЬ

Протекторы Гвинт Gwent Sleeves - Northern Realms (100 штук) 64х89 мм
Новинка
Протекторы Гвинт Gwent Sleeves - Northern Realms (100 штук) 64х89 мм
65 р.
Наличие:
КУПИТЬ

Счетчик жизней D20 (Разные цвета в ассортименте)
Счетчик жизней D20 (Разные цвета в ассортименте)
1 отзыв
3 р.
Наличие:
КУПИТЬ

Протекторы Премиум Pantheon Sleeves Standart Card Game Гермес Эпик 63.5x88 mm 55 шт. (SCG-101)
Протекторы Премиум Pantheon Sleeves Standart Card Game Гермес Эпик 63.5x88 mm 55 шт. (SCG-101)
5.90 р.
Наличие:
КУПИТЬ

Протекторы Гвинт Gwent Sleeves - Nilfgaard (100 штук) 64х89 мм
Новинка
Протекторы Гвинт Gwent Sleeves - Nilfgaard (100 штук) 64х89 мм
65 р.
Наличие:
КУПИТЬ
</p>
    """)
