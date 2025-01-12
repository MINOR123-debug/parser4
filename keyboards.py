from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)

# Клавіатура з кнопкою для пошуку
search_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Парсети👤", callback_data="parser")],
    [InlineKeyboardButton(text="Інформація 🔍", callback_data="info")],
])

open1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📋 Отримати список підписників", callback_data="sp")],
    [InlineKeyboardButton(text="🗑 очистити файл підписників", callback_data="op")]
    ])


bay = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🗑 очистити файл підписників", callback_data="op")],
])

bay1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Парсети заново 👤", callback_data="parser")],
])


admin_panel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🌟Активність🌟'),
                                      KeyboardButton(text='🌟Зробити росилку🌟')],
                                      [KeyboardButton(text='⏰Тех-перерва⏰'),
                                       KeyboardButton(text='👥Користувачі👥')],
                                      [KeyboardButton(text='🔓Активні доступи🔓'),
                                       KeyboardButton(text='🔐Надати доступ🔐')
                                    ]],
                        resize_keyboard=True,
                        input_field_placeholder='Виберете пункт в меню...')


vip = InlineKeyboardMarkup(inline_keyboard=[[
InlineKeyboardButton(text='Назад⚡️', callback_data='vip1')]])


admin_info = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Користувачі id'),
                                      KeyboardButton(text='Admin info')],
                                      [KeyboardButton(text='⚡️Назад⚡️')]])