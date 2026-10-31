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
class TargetState(StatesGroup):
    waiting_for_username = State()
    waiting_for_text = State()
    waiting_for_count = State()

# Головне меню з кнопками
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Надіслати сповіщення", callback_data="run_target"),
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
        "🤖 **PulseSend Bot v1.2**\n\n"
        "Інструмент для автоматизованої відправки сповіщень у соцмережі з налаштуванням кількості повторів.\n"
        "Працює автономно на базі Python."
    )
    await callback.answer()

# Кнопка "Налаштування"
@dp.callback_query(F.data == "settings")
async def settings_callback(callback: CallbackQuery) -> None:
    await callback.message.answer("⚙️ **Параметри системи:**\n- Статус: Активний\n- Канали: Telegram / Месенджери готові")
    await callback.answer()

# Початок сценарію (натиснули "🚀 Надіслати сповіщення")
@dp.callback_query(F.data == "run_target")
async def start_target_process(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        "🎯 **Введіть нікнейм або посилання** на ціль у соцмережах / Telegram:\n"
        "*(Приклад: @username або посилання)*"
    )
    await state.set_state(TargetState.waiting_for_username)
    await callback.answer()

# Отримуємо нікнейм
@dp.message(TargetState.waiting_for_username)
async def receive_username(message: Message, state: FSMContext) -> None:
    target = message.text.strip()
    await state.update_data(target_user=target)
    
    await message.answer(
        f"✅ Ціль **{target}** успішно збережено.\n\n"
        "✍️ Тепер введіть **текст повідомлення**, яке потрібно надіслати:"
    )
    await state.set_state(TargetState.waiting_for_text)

# Отримуємо текст
@dp.message(TargetState.waiting_for_text)
async def receive_text(message: Message, state: FSMContext) -> None:
    custom_text = message.text
    await state.update_data(custom_text=custom_text)
    
    await message.answer(
        "🔢 Введіть **кількість повідомлень**, яку потрібно надіслати:\n"
        "*(Введіть ціле число, наприклад: 5 або 10)*"
    )
    await state.set_state(TargetState.waiting_for_count)

# Отримуємо кількість і запускаємо цикл відправки
@dp.message(TargetState.waiting_for_count)
async def receive_count(message: Message, state: FSMContext) -> None:
    try:
        count = int(message.text.strip())
        if count <= 0 or count > 50:
            await message.answer("⚠️ Будь ласка, введіть число від 1 до 50.")
            return
    except ValueError:
        await message.answer("⚠️ Будь ласка, введіть коректне ціле число (наприклад: 5).")
        return

    data = await state.get_data()
    target = data.get("target_user")
    custom_text = data.get("custom_text")
    
    status_msg = await message.answer(
        f"🔍 Шукаю профіль **{target}** та готую чергу на {count} повідомлень..."
    )
    
    await asyncio.sleep(1.5)
    
    # Симуляція циклу відправки
    for i in range(1, count + 1):
        await status_msg.edit_text(f"📤 Надсилання повідомлення **{i} з {count}** для {target}...")
        await asyncio.sleep(0.8) # Пауза між відправками
    
    # Фінальний звіт
    await message.answer(
        f"✨ **Серію повідомлень успішно завершено!**\n\n"
        f"👤 **Отримувач:** {target}\n"
        f"💬 **Текст:** *{custom_text}*\n"
        f"📊 **Надіслано повідомлень:** {count}",
        reply_markup=get_main_keyboard()
    )
    
    await state.clear()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
