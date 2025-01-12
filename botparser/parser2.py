import json
import asyncio
from aiogram import Router, types
from aiogram.filters import CommandObject
from telethon import TelegramClient
from aiogram.filters import Command

import keyboards as kb

# Налаштування Telethon
API_ID = 20979523
API_HASH = "e8aa8ee24dbe98293f5bd124071d4f56"
PHONE_NUMBER = "+380631776515"

# Ініціалізація Telethon клієнта
client = TelegramClient("search_session", API_ID, API_HASH)


parser_router = Router()


user_parsing_state = {}


try:
    with open("pay.json", "r", encoding="utf-8") as f:
        allowed_users = json.load(f)
except FileNotFoundError:
    allowed_users = []

ADMIN_IDS = [1332517469, 6395768505]

def save_allowed_users():
    with open("pay.json", "w", encoding="utf-8") as f:
        json.dump(allowed_users, f, ensure_ascii=False, indent=4)

# Функція для підключення до Telethon
async def setup_telethon():
    """
    Ініціалізація та авторизація Telethon клієнта.
    """
    if not client.is_connected():
        await client.start(PHONE_NUMBER)
        print("Telethon успішно авторизовано!")

@parser_router.message(Command("add"))
async def add_user(message: types.Message, command: CommandObject):
    """
    Додає користувача до списку дозволених із записом до файлу pay.json. Доступно лише для адміністраторів.
    """
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас немає прав для виконання цієї команди.")
        return

    # Отримання ID користувача
    user_id = int(command.args.strip()) if command.args else None
    if not user_id:
        await message.answer("Вкажіть ID користувача. Використовуйте: /add ID")
        return

    # Завантаження існуючих даних із pay.json
    try:
        with open("pay.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        allowed_users = data.get("users", [])  # Отримуємо список користувачів
    except FileNotFoundError:
        allowed_users = []
    except json.JSONDecodeError:
        allowed_users = []

    # Перевірка, чи користувач уже має доступ
    if any(user["id"] == user_id for user in allowed_users):
        await message.answer("Цей користувач вже має доступ.")
        return

    # Додавання нового користувача
    new_user = {
        "id": user_id,
        "username": message.from_user.username or "Немає",
        "status": "активний"
    }
    allowed_users.append(new_user)

    # Збереження оновленого списку у файл pay.json
    data["users"] = allowed_users  # Оновлюємо список користувачів в структурі даних
    with open("pay.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Повідомлення адміністратора, що доступ надано користувачу (вказуємо нік користувача)
    await message.answer(f"(АДМІНОМ: @{new_user['username']}) надано доступ! Користувачу з ID {user_id} до платной функцій")

    # Надсилання повідомлення користувачу
    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=f"Вам надано доступ до функцій /parser адміністратором @{message.from_user.username}. \n"
                 "Тепер ви маєте платний контент, приємного користування 😊\n\n"
        )
    except Exception as e:
        await message.answer(f"Не вдалося повідомити користувача: {e}")



@parser_router.message(Command("addoff"))
async def remove_user(message: types.Message, command: CommandObject):
    """
    Видаляє користувача з файлу pay.json. Доступно лише для адміністраторів.
    """
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас немає прав для виконання цієї команди.")
        return

    user_id = int(command.args.strip()) if command.args else None
    if not user_id:
        await message.answer("Вкажіть ID користувача. Використовуйте: /addoff ID")
        return

    # Завантаження існуючих даних із pay.json
    try:
        with open("pay.json", "r", encoding="utf-8") as f:
            allowed_users = json.load(f).get("users", [])  # Завантажуємо список користувачів
    except FileNotFoundError:
        allowed_users = []
    except json.JSONDecodeError:
        allowed_users = []

    # Перевірка, чи користувач є в списку
    user = next((user for user in allowed_users if user["id"] == user_id), None)
    if not user:
        await message.answer("Цей користувач не має доступу.")
        return

    # Видаляємо користувача зі списку
    allowed_users = [user for user in allowed_users if user["id"] != user_id]

    # Зберігаємо оновлені дані у файл
    try:
        with open("pay.json", "w", encoding="utf-8") as f:
            json.dump({"users": allowed_users}, f, ensure_ascii=False, indent=4)
        await message.answer(f"Користувача з ID {user_id} видалено з файлу pay.json.")
    except Exception as e:
        await message.answer(f"Сталася помилка при збереженні файлу: {e}")

    # Надсилання повідомлення користувачу
    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=f"Ваш доступ до функцій було скасовано адміністратором {message.from_user.full_name}. \n"
                 "Ви більше не маєте доступу до цього бота. ✅"
        )
    except Exception as e:
        await message.answer(f"Не вдалося повідомити користувача: {e}")











from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup


@parser_router.callback_query(lambda c: c.data == "parser")
async def handle_parser_button(callback: CallbackQuery):
    """
    Обробка натискання кнопки з callback_data "parser".
    """
    user_id = callback.from_user.id

    # Перевірка доступу
    if user_id not in ADMINS:
        await callback.message.answer("❌ У вас немає доступу до цієї функції. Зверніться до адміністратора.")
        return

    # Просимо користувача надіслати посилання
    await callback.message.answer("📥 Відправте посилання на канал (має починатися з 'https://').")
    user_parsing_state[user_id] = {'awaiting_link': True}  # Ставимо стан очікування посилання


@parser_router.message(lambda message: message.text and message.text.startswith("https://") and not message.photo and not message.video)
async def handle_channel_link(message: types.Message):
    """
    Обробка повідомлення з посиланням на канал.
    """
    user_id = message.from_user.id

    # Перевіряємо, чи бот очікує посилання
    if not user_parsing_state.get(user_id, {}).get('awaiting_link'):
        return

    # Отримуємо посилання
    channel_url = message.text.strip()
    if not channel_url.startswith("https://") or "t.me/" not in channel_url:
        await message.answer("❌ Це неправильний формат посилання. Вкажіть правильне посилання (має починатися з 'https://').")
        return

    # Якщо посилання валідне, скидаємо стан очікування
    user_parsing_state[user_id]['awaiting_link'] = False

    # Запускаємо функцію парсингу
    await cmd_parser(message, CommandObject(args=channel_url))


async def cmd_parser(message: types.Message, command: CommandObject):
    """
    Основна функція парсингу.
    """
    user_id = message.from_user.id

    # Перевірка доступу
    if user_id not in ADMINS:
        await message.answer("❌ У вас немає доступу до цієї функції. Зверніться до адміністратора.")
        return

    # Отримання посилання з аргументів команди
    channel_url = command.args.strip() if command.args else None
    if not channel_url:
        await message.answer("❌ Ви не вказали посилання. Використовуйте: /parser https://t.me/назва_каналу")
        return

    if not channel_url.startswith("https://") or "t.me/" not in channel_url:
        await message.answer("❌ Це не правильний формат для посилання. Укажіть правильний формат.")
        return

    # Встановлення стану "парсинг"
    user_parsing_state[user_id] = {'parsing': True}

    try:
        # Переконуємося, що клієнт підключений
        if not client.is_connected():
            await setup_telethon()

        # Отримуємо канал
        channel = await client.get_entity(channel_url)

        # Ініціалізація списку підписників
        subscribers = []
        total_fetched = 0

        # Парсимо підписників із паузами
        async for user in client.iter_participants(channel):
            subscribers.append({
                "id": user.id,
                "username": user.username,
                "name": f"{user.first_name} {user.last_name}" if user.first_name else ""
            })
            total_fetched += 1

            if total_fetched % 2000 == 0:
                await message.answer(f"Спаршено {total_fetched} підписників. Процес триває, очікуйте ⏳.")
                await asyncio.sleep(5)

        # Зберігаємо підписників у JSON файл
        with open("subscribers.json", "w", encoding="utf-8") as f:
            json.dump(subscribers, f, ensure_ascii=False, indent=4)

        # Відправляємо результат
        await message.answer(f"✅ Спаршено {total_fetched} підписників! Ви можете отримати список або очистити його.", reply_markup=kb.open1)

    except Exception as e:
        await message.answer(f"❌ Сталася помилка: {e}")
        print(f"Помилка при парсингу: {e}")
    finally:
        user_parsing_state[user_id] = {'parsing': False}
        await message.answer("✔️ Процес парсингу завершено. Перед наступним запуском очистіть список за допомогою команди /clear.")





































from aiogram.types import CallbackQuery, Message

SUBSCRIBERS_FILE = "subscribers.json"

def read_subscribers():
    """
    Зчитує список підписників із файлу.
    """
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
            subscribers = json.load(file)
            return subscribers if isinstance(subscribers, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Список адміністраторів
ADMINS = [1332517469, 7689890294]  # Замініть на реальні ID адміністраторів

def clear_subscribers():
    """
    Очищає список підписників у файлі.
    """
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as file:
        json.dump([], file)


@parser_router.callback_query(lambda c: c.data == "sp")
async def handle_view_subscribers(callback: CallbackQuery):
    """
    Відображає список підписників із файлу.
    """
    user_id = callback.from_user.id

    # Перевірка прав адміністратора
    if user_id not in ADMINS:
        await callback.message.answer("У вас немає прав доступу до цієї функції. ❌")
        return

    # Читаємо список підписників із файлу
    try:
        with open("subscribers.json", "r", encoding="utf-8") as file:
            subscribers = json.load(file)
            if not isinstance(subscribers, list):
                await callback.message.answer("Формат файлу некоректний. Очікується список.")
                return
    except FileNotFoundError:
        await callback.message.answer("❌ Файл із підписниками не знайдено.")
        return
    except json.JSONDecodeError:
        await callback.message.answer("❌ Помилка читання файлу з підписниками.")
        return

    # Якщо список порожній
    if not subscribers:
        await callback.message.answer("Список підписників порожній.")
        return

    # Ліміт символів у повідомленні Telegram
    char_limit = 4000
    current_message = ""

    # Логування кількості підписників
    print(f"✅ Знайдено {len(subscribers)} підписників.")

    for subscriber in subscribers:
        # Отримуємо ID, username та name
        user_id = subscriber.get("id", "Невідомий ID")
        username = subscriber.get("username", "Без username")
        name = subscriber.get("name", "Без імені")

        # Форматуємо рядок для виведення
        formatted_message = f"ID: {user_id}\n@{username}\n{name}\n\n"

        # Перевірка ліміту символів перед відправкою
        if len(current_message) + len(formatted_message) <= char_limit:
            current_message += formatted_message
        else:
            # Надсилаємо частину повідомлення, якщо перевищено ліміт
            await callback.message.answer(current_message)
            current_message = formatted_message

            await asyncio.sleep(1)

    # Надсилаємо залишок, якщо він є
    if current_message:
        await callback.message.answer(current_message)

    # Повідомлення про завершення
    await callback.message.answer("✅ Список підписників виданий." , reply_markup=kb.bay)


# Обробник для callback_data
@parser_router.callback_query(lambda c: c.data == "op")
async def handle_clear_subscribers(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Перевірка доступу
    if user_id not in ADMINS:
        await callback.message.answer("У вас немає прав доступу до цієї функції. ❌")
        return

    # Очищаємо список підписників
    clear_subscribers()

    # Повідомлення про успішне очищення
    await callback.message.answer("✅ Список підписників очищено! можете спарсити ще раз✅" , reply_markup=kb.bay1)


#файл 

from aiogram.types.input_file import InputFile
from aiogram.types.input_file import FSInputFile
import json
import os


EXPORT_FILE = "exported_subscribers.txt"  # Файл для експорту

# Функція для читання підписників
def read_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file) if isinstance(json.load(file), list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Функція для створення файлу з підписниками
def create_export_file():
    subscribers = read_subscribers()
    with open(EXPORT_FILE, "w", encoding="utf-8") as file:
        for subscriber in subscribers:
            # Формат запису в файл
            user_id = subscriber.get("id", "Невідомий ID")
            username = subscriber.get("username", "Без username")
            name = subscriber.get("name", "Без імені")
            file.write(f"ID: {user_id}\nІм'я: {name}\nЮзернейм: @{username}\n\n")

# Обробник для callback_data 'fp'
@parser_router.callback_query(lambda c: c.data == "fp")
async def handle_export_subscribers(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Перевірка доступу
    if user_id not in ADMINS:
        await callback.message.answer("У вас немає прав доступу до цієї функції. ❌")
        return

    # Створення файлу для експорту
    create_export_file()

    # Перевірка існування файлу
    if os.path.exists(EXPORT_FILE) and os.path.getsize(EXPORT_FILE) > 0:
        # Відправка файлу користувачу
        file_to_send = FSInputFile(EXPORT_FILE)  # Використовуємо FSInputFile для передачі файлу
        await callback.message.answer_document(file_to_send, caption="📂 Ось файл з підписниками.")
    else:
        await callback.message.answer("❌ Не вдалося знайти файл для експорту.")