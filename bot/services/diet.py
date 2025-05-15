from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ReplyKeyboardRemove
from bot.database.sqlite_db import DatabaseManager
from bot.utils.excel_export import export_to_excel
from bot.settings.setup_bot import dp
from bot.states.states import ParticipantStates
from bot.utils.logger import log_info, log_error, log_warning
from bot.utils.utils import send_with_progress
from bot.keyboards.keyboards import get_back_keyboard, get_limitations_keyboard, get_eating_schedule_keyboard, get_diet_preferences_keyboard, \
    get_allergies_keyboard, get_cooking_time_keyboard, get_recipe_format_keyboard, \
    get_sports_nutrition_experience_keyboard, get_tracking_history_keyboard, get_program_priorities_keyboard, get_additional_info_keyboard



@dp.message_handler(state=ParticipantStates.WAITING_FOR_EATING_SCHEDULE)
async def process_eating_schedule(message: types.Message, state: FSMContext):
    """Обработка режима питания"""
    log_info(f"process_eating_schedule | message: {message.text}")

    if message.text == "⬅️ Назад":
        user_data = await state.get_data()
        if user_data.get("has_limitations") == "Да":
            await ParticipantStates.WAITING_FOR_LIMITATIONS_DETAILS.set()
            await send_with_progress(message, state, "Опиши свои ограничения или особенности (травмы, боли):", reply_markup=get_back_keyboard())

        else:
            await ParticipantStates.WAITING_FOR_LIMITATIONS.set()
            await send_with_progress(message, state, "Имеются ли ограничения или особенности (травмы, боли)?", reply_markup=get_limitations_keyboard())
        return

    eating_schedule = message.text.strip()

    valid_schedules = [
        "Трехразовое питание", 
        "Пятиразовое питание", 
        "Частые перекусы", 
        "Другой режим"
    ]
    
    if eating_schedule not in valid_schedules:
        await message.answer("Пожалуйста, выбери режим питания из предложенных вариантов.")
        return

    await state.update_data(eating_schedule=eating_schedule)
    
    # Если выбран "Другой режим", запросим текстовое описание
    if eating_schedule == "Другой режим":
        await ParticipantStates.WAITING_FOR_EATING_SCHEDULE_DETAIL.set()
        await message.answer("Опиши свой режим питания:", reply_markup=get_back_keyboard())
        return

    # После выбора режима питания — следующий шаг
    await ParticipantStates.WAITING_FOR_DIET_PREFERENCES.set()
    await send_with_progress(message, state, "Есть ли у тебя диетические предпочтения?", reply_markup=get_diet_preferences_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_EATING_SCHEDULE_DETAIL)
async def process_eating_schedule_detail(message: types.Message, state: FSMContext):
    """Обработка текста при выборе «Другой режим»"""
    log_info(f"process_eating_schedule_detail | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_EATING_SCHEDULE.set()
        await send_with_progress(
            message, state,
            "Какой режим питания для тебя привычен?",
            reply_markup=get_eating_schedule_keyboard()
        )
        return

    detail = message.text.strip()
    if len(detail) < 3:
        return await message.answer("Опиши, пожалуйста, режим подробнее.")

    await state.update_data(eating_schedule_detail=detail)

    # Переходим дальше
    await ParticipantStates.WAITING_FOR_DIET_PREFERENCES.set()
    await send_with_progress(
        message, state,
        "Есть ли у тебя диетические предпочтения?",
        reply_markup=get_diet_preferences_keyboard()
    )



@dp.message_handler(state=ParticipantStates.WAITING_FOR_DIET_PREFERENCES)
async def process_diet_preferences(message: types.Message, state: FSMContext):
    """Обработка диетических предпочтений"""
    log_info(f"process_diet_preferences | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_EATING_SCHEDULE.set()
        await send_with_progress(message, state, "Какой режим питания для тебя привычен?", reply_markup=get_eating_schedule_keyboard())
        return

    diet_preferences = message.text.strip()

    valid_preferences = ["Без ограничений", "Вегетарианство", "Веганство", 
                        "Без глютена", "Без молочных продуктов", "Другие"]
    
    if diet_preferences not in valid_preferences:
        await message.answer("Пожалуйста, выбери диетические предпочтения из предложенных вариантов.")
        return

    await state.update_data(diet_preferences=diet_preferences)

    if diet_preferences == "Другие":
        await ParticipantStates.WAITING_FOR_DIET_DETAILS.set()
        await message.answer("Опиши свои диетические предпочтения:", reply_markup=get_back_keyboard())
    else:
        await ParticipantStates.WAITING_FOR_ALLERGIES.set()
        await send_with_progress(message, state, "Есть ли у тебя аллергии или непереносимость продуктов?", reply_markup=get_allergies_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_DIET_DETAILS)
async def process_diet_details(message: types.Message, state: FSMContext):
    """Обработка деталей диетических предпочтений"""
    log_info(f"process_diet_details | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_DIET_PREFERENCES.set()
        await send_with_progress(message, state, "Есть ли у тебя диетические предпочтения?", reply_markup=get_diet_preferences_keyboard())

        return

    diet_details = message.text.strip()
    
    # Минимальная проверка
    if len(diet_details) < 3:
        await message.answer("Пожалуйста, опиши подробнее свои диетические предпочтения.")
        return

    await state.update_data(diet_details=diet_details)

    await ParticipantStates.WAITING_FOR_ALLERGIES.set()
    await send_with_progress(message, state, "Есть ли у тебя аллергии или непереносимость продуктов?", reply_markup=get_allergies_keyboard())



@dp.message_handler(state=ParticipantStates.WAITING_FOR_ALLERGIES)
async def process_allergies(message: types.Message, state: FSMContext):
    """Обработка наличия аллергий"""
    log_info(f"process_allergies | message: {message.text}")
    if message.text == "⬅️ Назад":
        user_data = await state.get_data()
        diet_preferences = user_data.get("diet_preferences")
        
        if diet_preferences == "Другие":
            await ParticipantStates.WAITING_FOR_DIET_DETAILS.set()
            await message.answer("Опиши свои диетические предпочтения:", reply_markup=get_back_keyboard())
        else:
            await ParticipantStates.WAITING_FOR_DIET_PREFERENCES.set()
            await send_with_progress(message, state, "Есть ли у тебя диетические предпочтения?", reply_markup=get_diet_preferences_keyboard())
        return

    allergies = message.text.strip()

    if allergies not in ["Да", "Нет"]:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(has_allergies=allergies)

    if allergies == "Да":
        await ParticipantStates.WAITING_FOR_ALLERGIES_DETAILS.set()
        await message.answer("Опиши свои аллергии или непереносимость продуктов:", 
                           reply_markup=get_back_keyboard())
    else:
        await ParticipantStates.WAITING_FOR_COOKING_TIME.set()
        await send_with_progress(message, state, "Сколько ты времени готов(а) уделять приготовлению еды ежедневно?", reply_markup=get_cooking_time_keyboard())
    


@dp.message_handler(state=ParticipantStates.WAITING_FOR_ALLERGIES_DETAILS)
async def process_allergies_details(message: types.Message, state: FSMContext):
    """Обработка деталей аллергий"""
    log_info(f"process_allergies_details | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_ALLERGIES.set()
        await message.answer("Есть ли у тебя аллергии или непереносимость продуктов?", 
                           reply_markup=get_allergies_keyboard())
        return

    allergies_details = message.text.strip()
    
    # Минимальная проверка
    if len(allergies_details) < 3:
        await message.answer("Пожалуйста, опиши подробнее свои аллергии или непереносимость продуктов.")
        return

    await state.update_data(allergies_details=allergies_details)

    await ParticipantStates.WAITING_FOR_COOKING_TIME.set()
    await send_with_progress(message, state, "Сколько ты времени готов(а) уделять приготовлению еды ежедневно?", reply_markup=get_cooking_time_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_COOKING_TIME)
async def process_cooking_time(message: types.Message, state: FSMContext):
    log_info(f"process_cooking_time | message: {message.text}")

    if message.text == "⬅️ Назад":
        user_data = await state.get_data()
        if user_data.get("has_allergies") == "Да":
            # 1) Переводим в нужный стейт
            await ParticipantStates.WAITING_FOR_ALLERGIES_DETAILS.set()
            # 2) Шлём вопрос через send_with_progress, чтобы было (18/26)
            await send_with_progress(
                message, state,
                "Опиши свои аллергии или непереносимость продуктов:",
                reply_markup=get_back_keyboard()
            )
        else:
            await ParticipantStates.WAITING_FOR_ALLERGIES.set()
            await send_with_progress(
                message, state,
                "Есть ли у тебя аллергии или непереносимость продуктов?",
                reply_markup=get_allergies_keyboard()
            )
        return
    
    cooking_time = message.text.strip()

    valid_times = ["До 15 минут", "15-30 минут", "30-45 минут", "Более 45 минут"]
    
    if cooking_time not in valid_times:
        await message.answer("Пожалуйста, выбери время приготовления из предложенных вариантов.")
        return

    await state.update_data(cooking_time=cooking_time)

    await ParticipantStates.WAITING_FOR_RECIPE_FORMAT.set()
    await send_with_progress(message, state, "Какой формат рецептов для тебя удобнее?", reply_markup=get_recipe_format_keyboard())



@dp.message_handler(state=ParticipantStates.WAITING_FOR_RECIPE_FORMAT)
async def process_recipe_format(message: types.Message, state: FSMContext):
    log_info(f"process_recipe_format | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_COOKING_TIME.set()
        await send_with_progress(
            message, state,
            "Сколько ты времени готов(а) уделять приготовлению еды ежедневно?",
            reply_markup=get_cooking_time_keyboard()
        )
        return

    recipe_format = message.text.strip()
    valid_formats = [
        "Пошаговые рецепты с фото",
        "Простой список ингредиентов и инструкции",
        "Видеорецепты",
        "Другой формат"
    ]
    if recipe_format not in valid_formats:
        await message.answer("Пожалуйста, выбери формат рецептов из предложенных вариантов.")
        return

    await state.update_data(recipe_format=recipe_format)

    if recipe_format == "Другой формат":
        await ParticipantStates.WAITING_FOR_RECIPE_FORMAT_DETAILS.set()
        await send_with_progress(
            message, state,
            "Опиши удобный для тебя формат рецептов:",
            reply_markup=get_back_keyboard()
        )
    else:
        # вопрос 21
        await ParticipantStates.WAITING_FOR_TRACKING_HISTORY.set()
        await send_with_progress(
            message, state,
            "Хотел(а) бы ты вести историю изменений веса, параметры тела, достижения в тренировках?",
            reply_markup=get_tracking_history_keyboard()
        )


@dp.message_handler(state=ParticipantStates.WAITING_FOR_RECIPE_FORMAT_DETAILS)
async def process_recipe_format_details(message: types.Message, state: FSMContext):
    """Обработка деталей формата рецептов"""
    log_info(f"process_recipe_format_details | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_RECIPE_FORMAT.set()
        await send_with_progress(message, state, "Какой формат рецептов для тебя удобнее?", reply_markup=get_recipe_format_keyboard())

        return

    recipe_format_details = message.text.strip()
    
    if len(recipe_format_details) < 3:
        await message.answer("Пожалуйста, опиши подробнее предпочитаемый формат рецептов.")
        return

    await state.update_data(recipe_format_details=recipe_format_details)
    
    await ParticipantStates.WAITING_FOR_TRACKING_HISTORY.set()
    await send_with_progress(message, state, "Хотел(а) бы ты вести историю изменений веса, параметры тела, достижения в тренировках?", reply_markup=get_tracking_history_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRACKING_HISTORY)
async def process_tracking_history(message: types.Message, state: FSMContext):
    """Обработка вопроса о ведении истории изменений"""
    log_info(f"process_tracking_history | message: {message.text}")
    if message.text == "⬅️ Назад":
        user_data = await state.get_data()
        recipe_format = user_data.get("recipe_format")
        if recipe_format == "Другой формат":
            await ParticipantStates.WAITING_FOR_RECIPE_FORMAT_DETAILS.set()
            await send_with_progress(message, state, "Опиши удобный для тебя формат рецептов:", reply_markup=get_back_keyboard())
        else:
            await ParticipantStates.WAITING_FOR_RECIPE_FORMAT.set()
            await send_with_progress(message, state, "Какой формат рецептов для тебя удобнее?", reply_markup=get_recipe_format_keyboard())
        return

    tracking_history = message.text.strip()

    valid_answers = ["Да", "Нет"]
    
    if tracking_history not in valid_answers:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(tracking_history=tracking_history)

    # Следующий вопрос должен быть 22 (WAITING_FOR_PROGRAM_PRIORITIES)
    await ParticipantStates.WAITING_FOR_PROGRAM_PRIORITIES.set()
    await send_with_progress(
        message, state,
        "Что для тебя наиболее важно в программе?",
        reply_markup=get_program_priorities_keyboard()
    )


@dp.message_handler(state=ParticipantStates.WAITING_FOR_PROGRAM_PRIORITIES)
async def process_program_priorities(message: types.Message, state: FSMContext):
    """Обработка вопроса о приоритетах в программе"""
    log_info(f"process_program_priorities | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRACKING_HISTORY.set()
        await send_with_progress(message, state, "Хотел(а) бы ты вести историю изменений веса, параметры тела, достижения в тренировках?", reply_markup=get_tracking_history_keyboard())
        return

    program_priority = message.text.strip()

    valid_priorities = ["Простота и понятность", "Результативность и быстрые изменения", 
                      "Гибкость (можно менять программу в зависимости от ситуации)", 
                      "Баланс между тренировками и питанием", "Доступность (необходимые продукты и тренировки)"]
    
    if program_priority not in valid_priorities:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(program_priority=program_priority)

    await ParticipantStates.WAITING_FOR_ADDITIONAL_INFO.set()
    await send_with_progress(message, state, "Есть ли что-то еще, что ты хотел(а) бы добавить или уточнить?", reply_markup=get_additional_info_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_ADDITIONAL_INFO)
async def process_additional_info(message: types.Message, state: FSMContext):
    """Обработка дополнительной информации от пользователя"""
    log_info(f"process_additional_info | message: {message.text}")
    
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_PROGRAM_PRIORITIES.set()
        await send_with_progress(
            message, state,
            "Что для тебя наиболее важно в программе?",
            reply_markup=get_program_priorities_keyboard()
        )
        return

    additional_info = message.text.strip()
    await state.update_data(additional_info=additional_info)

    await ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE.set()
    await send_with_progress(
        message, state,
        "Пробовал ли ты когда-либо употребление спортивного питания?",
        reply_markup=get_sports_nutrition_experience_keyboard()
    )