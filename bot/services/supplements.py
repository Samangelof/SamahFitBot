

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot.settings.setup_bot import dp, bot
from bot.settings.config import ADMIN_CHAT_ID
from bot.database import sqlite_db
from bot.states.states import ParticipantStates
from aiogram.types import InputFile
from bot.utils.logger import log_info, log_error, log_warning
from bot.utils.utils import send_with_progress
from bot.settings.setup_bot import db
from bot.keyboards.keyboards import (
    get_sports_nutrition_types_keyboard, 
    get_sports_nutrition_experience_keyboard, 
    get_additional_info_keyboard,
    get_sports_nutrition_budget_keyboard,
    get_sports_nutrition_types_skip_keyboard,
    get_back_keyboard
)


@dp.message_handler(state=ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE)
async def process_sports_nutrition_experience(message: types.Message, state: FSMContext):
    log_info(f"process_sports_nutrition_experience | message: {message.text}")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_ADDITIONAL_INFO.set()
        await send_with_progress(
            message, state,
            "Есть ли что-то еще, что ты хотел(а) бы добавить или уточнить?",
            reply_markup=get_additional_info_keyboard()
        )
        return

    exp = message.text.strip()
    if exp not in ["Да", "Нет"]:
        return await message.answer("Пожалуйста, выбери один из предложенных вариантов.")

    await state.update_data(sports_nutrition_experience=exp)
    await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_TYPES.set()

    if exp == "Нет":
        await send_with_progress(
            message, state,
            "Что пробовал из спортивного питания?",
            reply_markup=get_sports_nutrition_types_skip_keyboard()
        )
    else:
        await send_with_progress(
            message, state,
            "Что пробовал из спортивного питания?",
            reply_markup=get_sports_nutrition_types_keyboard()
        )




@dp.message_handler(state=ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_TYPES)
async def process_sports_nutrition_types(message: types.Message, state: FSMContext):
    log_info(f"process_sports_nutrition_types | message: {message.text}")

    # назад
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE.set()
        await send_with_progress(
            message, state,
            "Пробовал ли ты когда-либо употребление спортивного питания?",
            reply_markup=get_sports_nutrition_experience_keyboard()
        )
        return

    if message.text == "Пропустить":
        await state.update_data(sports_nutrition_types="—")
        await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_BUDGET.set()
        await send_with_progress(
            message, state,
            "Позволяет ли бюджет купить спортивное питание?",
            reply_markup=get_sports_nutrition_budget_keyboard()
        )
        return
    
    # ввод “Другие добавки”
    if message.text == "Другие добавки":
        await message.answer(
            "Укажи, какие другие добавки ты пробовал:\n\nКогда закончишь — нажми 'Далее'.",
            reply_markup=get_sports_nutrition_types_keyboard()
        )
        return

    # обработка “Далее”
    if message.text == "Далее":
        data = await state.get_data()
        if not data.get("sports_nutrition_types"):
            return await message.answer("Пожалуйста, выбери хотя бы один вариант или вернись назад.")
        await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_BUDGET.set()
        await send_with_progress(
            message, state,
            "Позволяет ли бюджет купить спортивное питание?",
            reply_markup=get_sports_nutrition_budget_keyboard()
        )
        return

    # добавление обычного варианта
    if message.text in ["Протеины", "Креатин", "BCAA", "Гейнеры", "Жиросжигатели"]:
        data = await state.get_data()
        types_list = data.get("sports_nutrition_types", [])
        if message.text not in types_list:
            types_list.append(message.text)
            await state.update_data(sports_nutrition_types=types_list)
        return await message.answer(
            f"Добавлено: {message.text}\nВыбери ещё или нажми 'Далее'",
            reply_markup=get_sports_nutrition_types_keyboard()
        )

    await message.answer("Пожалуйста, выбери один из предложенных вариантов или нажми 'Далее'.")





@dp.message_handler(state=ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_BUDGET)
async def process_sports_nutrition_budget(message: types.Message, state: FSMContext):
    """Обработка вопроса о бюджете на спортивное питание"""
    log_info(f"process_sports_nutrition_budget | message: {message.text}")
    if message.text == "⬅️ Назад":
        user_data = await state.get_data()
        if user_data.get("sports_nutrition_experience") == "Да":
            await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_TYPES.set()
            await send_with_progress(message, state, "Что пробовал из спортивного питания?", reply_markup=get_sports_nutrition_types_keyboard())
        else:
            await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE.set()
            await send_with_progress(message, state, "Пробовал ли ты когда-либо употребление спортивного питания?", reply_markup=get_sports_nutrition_experience_keyboard())
        return

    sports_nutrition_budget = message.text.strip()

    valid_budgets = ["Да, без проблем", "Иногда могу позволить себе", "Нет, это слишком дорого"]
    
    if sports_nutrition_budget not in valid_budgets:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(sports_nutrition_budget=sports_nutrition_budget)

    # Получаем все данные пользователя из состояния
    user_data = await state.get_data()
    
    # Форматируем данные для отправки админу
    # formatted_application = format_application(user_data)
    
    # -- Сохраняем данные пользователя в БД --
    # Добавляем пользователя в БД или обновляем его данные
    db.add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code
    )
    
    # Сохраняем заявку
    application_id = db.save_application(message.from_user.id, user_data)
    
    # Отправляем пользователю сообщение об успешном завершении анкеты
    await message.answer(
        "Спасибо за ответы! Теперь мы можем составить для тебя индивидуальную программу.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    
    try:
        video_path = InputFile("bot/roundles/final.mp4")
        await message.answer_video_note(video_path)
        
        await message.answer("Ты почти у цели! Осталось сделать последний шаг - оплата программы.")
    except Exception as e:
        log_info(f"Ошибка при отправке мотивационного сообщения: {e}")
    
    from bot.services.payment_service import generate_payment_link
    await generate_payment_link(message, state, application_id)


    log_info(f"Завершена анкета с данными: {user_data}")
    log_info(f"ID заявки: {application_id}")
    log_info(f"!--ЗАВЕРШЕНО--!")
    
    await state.finish()