import json
import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import search_menu
from aiogram.filters import Command

command_router = Router()

# Шлях до файлу з даними користувачів
users_file = "users.json"

# Функція для збереження користувача у файл
def save_user_data(user_id, username, first_name):
    try:
        # Завантажуємо існуючі дані
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        # Якщо файл не існує, створюємо порожній список
        users = []

    # Перевіряємо, чи користувач уже є у списку
    for user in users:
        if user["id"] == user_id:
            return  # Якщо користувач уже є, не додаємо його знову

    # Додаємо нового користувача
    users.append({
        "id": user_id,
        "username": username,
        "first_name": first_name
    })

    # Зберігаємо оновлені дані у файл
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

@command_router.message(CommandStart())
async def start_command(message: Message):
    """
    Обробник команди /start.
    """
    # Зберігаємо дані користувача
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    save_user_data(user_id, username, first_name)

    # Відправляємо відповідь користувачу
    await message.answer(
        f"Привіт, {message.from_user.first_name}! 👋\n"
        "Я допоможу тобі збірати підписників з каналу в список телеграм💬\n"
        "по кнопці ниже⬇️ ти можеш подивитися весь функціонал Бота🌟\n"
        "\n", reply_markup=search_menu,
    )


@command_router.callback_query(F.data == "info")
async def cmd_info(callback: CallbackQuery):
    await callback.answer('info')
    await callback.message.answer(f"Функціонал Бота🤖 \n"
                                  "бот вміє парсити підписників в телеграм,\n"
                                  "бот збирає лише публічні дані корисутвача з каналів силку на який ви кинули\n"


                                  
                                  )






# Реєстрація хендлера для команди /privacy
@command_router.message(Command("privacy"))
async def send_privacy_policy(message: Message):
    await message.answer(f"\n"
                         f"\n"
                         f"1. Які дані збирає бот?\n"
                         f"Наш бот автоматично збирає **лише дані, які є публічно доступними для інших користувачів у Telegram**. Зокрема:\n"       
                         f"- **Telegram ID**: Унікальний ідентифікатор, який використовується для ідентифікації користувача.\n"
                         f"- **Ім'я користувача**: Ваше публічне ім'я в Telegram (якщо воно доступне).\n"
                         f"- **Username** (нікнейм): Якщо ви маєте публічний username, бот може використовувати його для звернень до вас.\n"
                         f"- **Повідомлення, які ви відправляєте в бот**.\n"
                         f"\n"
                         f"Важливо:\n"
                         f"Бот працює лише з тими даними, які доступні будь-якому іншому користувачеві в Telegram.\n"
                         f"Бот **не отримує приватні дані**, такі як номери телефонів, електронні адреси чи інші конфіденційні дані.\n"
                         f"Усі зібрані дані є публічними і доступними в межах роботи Telegram.\n"
                  
                       

    
    
    
    
    
    
    
    )




# Список ID адміністраторів
ADMINS = [1332517469 , 6395768505] # Замість цих ID вставте реальні ID ваших адміністраторів

@command_router.message(Command("list"))
async def command_piplist(message: Message):
    # Перевірка чи користувач є адміном
    if message.from_user.id in ADMINS:
        await message.answer(
            "Command - /start 'запуск і перезапуск бота'\n"
            "\n"
            "Command - /help 'Підтримка в боті'\n"
            "\n"
            "Command - /sendall 'команда для розсилки-реклами'\n"
            "\n"
            "Command - /piplist 'видання підписників у списку'\n"
            "\n"
            "Command - /clear 'очищення списку підписників'\n"
            "\n"
            "Command - /reply 'відповідь на проблему тільки адмінам!'\n"
            "\n"
            "Command - /list 'подивитися список команди' \n"
            "\n"
            "Command - /admin 'адмін панель для легкого використання'\n"
            "\n"
            "Commаnd - /add ID 'видає права на доступ до функцій /parser'\n"
            "\n"
            "Commаnd - /addoff ID 'забирає доступ до функцій /parser'\n"
            "\n"
            "Commаnd - /online 'по цій команді ви можете переглянути активність користувачів в боті'\n"
            "\n"
            "Commаnd - /maintenance 'по цій команді ви можете запустити автоматичну перевірку бота щоби оникнути помилок'\n"
            "\n"
            "Commаnd - /list_users 'ця команда показує вам всю кількість людей в боті з бази даних'\n"
            "\n"
            "Commаnd - /addinfo 'переглянути всі активні сеанси на доступ до /parser'\n"
            "\n")
    else:
        await message.answer("У вас немає доступу до цієї команди. ❌")