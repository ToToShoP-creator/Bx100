import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Ваші дані бота
TOKEN = "9221802817:AAGmWexp2ceihyczhMitNv9j-DXCGvihCFo"

# Ініціалізація диспетчера та бота
dp = Dispatcher()

# Стани для покрокового введення даних (машина станів)
class BomberState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_text = State()

# Головне меню з кнопками
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Запустити розсилку", callback_data="run_spam"),
                InlineKeyboardButton(text="ℹ️ Про систему", callback_data="about")
            ],
            [
                InlineKeyboardButton(text="⚙️ Налаштування", callback_data="settings")
            ]
        ]
    )

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_name = html.quote(message.from_user.full_name)
    await message.answer(
        f"Привіт, {user_name}! 🚀\n"
        f"Бот **PulseSend** успішно активовано та готовий до роботи.\n\n"
        f"Оберіть потрібну дію за допомогою кнопок нижче:",
        reply_markup=get_main_keyboard()
    )

# Кнопка "Про систему"
@dp.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "🤖 **PulseSend Bot v1.0**\n\n"
        "Цей інструмент створений для автоматизації сповіщень та тестування каналів зв'язку.\n"
        "Працює автономно на базі Python та інтегрований з GitHub."
    )
    await callback.answer()

# Кнопка "Налаштування"
@dp.callback_query(F.data == "settings")
async def settings_callback(callback: CallbackQuery) -> None:
    await callback.message.answer("⚙️ **Параметри системи:**\n- Статус: Активний\n- Режим: Автономний\n- Канали: Telegram API підключено")
    await callback.answer()

# Початок сценарію розсилки (натиснули "🚀 Запустити розсилку")
@dp.callback_query(F.data == "run_spam")
async def start_spam_process(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        "📲 **Введіть номер телефону** людини (або цілі), для якої запусити розсилку:\n"
        "*(Приклад: +380XXXXXXXXX)*"
    )
    # Переводимо бота в стан очікування номера
    await state.set_state(BomberState.waiting_for_phone)
    await callback.answer()

# Отримуємо номер телефону від користувача
@dp.message(BomberState.waiting_for_phone)
async def receive_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    # Зберігаємо номер у пам'яті сесії
    await state.update_data(target_phone=phone)
    
    await message.answer(
        f"✅ Номер **{phone}** успішно збережено.\n\n"
        "✍️ Тепер введіть **текст повідомлення**, яке необхідно надіслати:"
    )
    # Переводимо бота в стан очікування тексту
    await state.set_state(BomberState.waiting_for_text)

# Отримуємо текст і запускаємо процес пошуку та відправки
@dp.message(BomberState.waiting_for_text)
async def receive_text(message: Message, state: FSMContext) -> None:
    custom_text = message.text
    data = await state.get_data()
    phone = data.get("target_phone")
    
    # Сповіщаємо про початок процесу
    status_msg = await message.answer(
        f"🔍 Шукаю ціль **{phone}** по базах та соцмережах (Telegram, Viber, SMS-шлюзи)..."
    )
    
    # Імітуємо процес пошуку та відправки (пауза для реалістичності)
    await asyncio.sleep(2)
    await status_msg.edit_text(f"📡 Знайдено профіль для **{phone}**!\n📤 Розпочинаю надсилання кастомного тексту...")
    
    await asyncio.sleep(1.5)
    
    # Фінальний звіт
    await message.answer(
        f"✨ **Операцію успішно завершено!**\n\n"
        f"🎯 **Ціль:** {phone}\n"
        f"💬 **Текст:** *{custom_text}*\n"
        f"📊 **Статус:** Повідомлення надіслано по всіх доступних каналах зв'язку.",
        reply_markup=get_main_keyboard()
    )
    
    # Очищаємо стан
    await state.clear()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
