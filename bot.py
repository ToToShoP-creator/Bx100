import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Ваші дані бота
TOKEN = "9221802817:AAGmWexp2ceihyczhMitNv9j-DXCGvihCFo"
OWNER_CHAT_ID = 9221802817

# Ініціалізація диспетчера та бота
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обробник команди /start.
    Вітає користувача та підтверджує, що бот успішно запущений.
    """
    user_name = html.quote(message.from_user.full_name)
    await message.answer(
        f"Привіт, {user_name}! 🚀\n"
        f"Бот **PulseSend** успішно активовано та готовий до роботи.\n\n"
        f"Незабаром тут з'являться додаткові кнопки та функції управління."
    )

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Приклад простого обробника повідомлень (ехо).
    У майбутньому сюди можна додати логіку бомбера / розсилки.
    """
    try:
        # Поки що бот просто відповідає на будь-яке текстове повідомлення
        await message.answer(f"Отримано ваше повідомлення: {message.text}")
    except TypeError:
        await message.answer("Схоже, сталася помилка при обробці повідомлення.")

async def main() -> None:
    # Ініціалізація бота з налаштуваннями за замовчуванням (ParseMode HTML)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Запуск поллінгу (опитування серверів Telegram на наявність нових повідомлень)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
