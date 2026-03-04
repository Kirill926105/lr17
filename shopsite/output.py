import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsite.settings')
django.setup()

from shop.models import Category

def manual_add_category():
    print("--- Программа добавления категории товаров ---")
    
    # Ввод данных с пояснениями
    name = input("Введите название новой категории (например, 'Игровые консоли'): ")
    description = input("Введите краткое описание категории: ")
    
    # Создание записи в БД
    new_cat = Category.objects.create(name=name, description=description)
    
    # Вывод результата с пояснениями
    print("\n--- Результат выполнения ---")
    print(f"Объект успешно сохранен в базе данных!")
    print(f"ID новой записи: {new_cat.id}")
    print(f"Название категории: {new_cat.name}")

if __name__ == "__main__":
    manual_add_category()