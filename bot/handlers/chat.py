from aiogram import types
from bot.settings.setup_bot import dp

from bot.services.openai_client import openai_client
from bot.states.states import ParticipantStates


user_chat_history = {}

# Обработчик команды /reset_chat - доступен только после анкеты
@dp.message_handler(commands=["reset_chat"], state=None)
async def reset_chat(message: types.Message):
    """Сброс истории чата"""
    user_id = message.from_user.id
    
    if user_id in user_chat_history:
        user_chat_history[user_id] = []
    
    await message.answer("История чата очищена. Вы можете начать новый диалог.")

# Обработчик текстовых сообщений для AI (только когда state=None - анкета завершена)
@dp.message_handler(state=None)
async def handle_text_message(message: types.Message):
    """Общение с AI после анкеты"""
    user_id = message.from_user.id
    user_text = message.text
    
    # Игнорируем любые команды кроме /chat и /reset_chat
    if user_text.startswith("/"):
        return
    
    # Инициализируем историю для пользователя, если её нет
    if user_id not in user_chat_history:
        user_chat_history[user_id] = []
        await message.answer("Здравствуйте! Я консультант. Чем могу помочь?")
        return
    
    # Получаем ответ от OpenAI
    response = await openai_client.generate_response(
        user_message=user_text,
        history=user_chat_history[user_id]
    )
    
    # Сохраняем историю
    user_chat_history[user_id].extend([
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": response}
    ])
    
    
    await message.answer(response)