from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


help_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Инструкция")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


