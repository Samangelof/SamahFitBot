from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InputFile
from bot.settings.setup_bot import dp
from bot.states.states import ParticipantStates
from bot.utils.logger import log_info 
from bot.utils.utils import send_with_progress
from bot.utils.debug_log import log_user_input, log_fsm_state
from bot.keyboards.keyboards import get_back_keyboard, get_training_time_keyboard, get_training_location_keyboard, \
    get_fitness_level_keyboard, get_training_frequency_keyboard, get_training_types_keyboard, get_training_duration_keyboard, \
    get_limitations_keyboard, get_eating_schedule_keyboard, get_training_goals_keyboard, get_physical_condition_keyboard


@dp.message_handler(state=ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION)
async def process_physical_condition(message: types.Message, state: FSMContext):
    """Обработка физической формы"""
    log_user_input(message, label="PHYSICAL_CONDITION")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_WEIGHT.set()
        await message.answer("Какой у тебя вес в килограммах?", reply_markup=get_back_keyboard())
        return

    physical_condition = message.text.strip()

    if physical_condition not in ["Худое телосложение", "Спортивного телосложения", "Имею лишние кг", "Свой вариант"]:
        await message.answer("Пожалуйста, выбери одну из предложенных опций.")
        return

    if physical_condition == "Свой вариант":
        await ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION_DETAILS.set()
        await message.answer("Опиши, пожалуйста, свое телосложение подробно:")
        return

    await state.update_data(physical_condition=physical_condition)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_TRAINING_GOALS.set()
    await send_with_progress(message, state, "Тренировочные предпочтения и цели?", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выбери тренировочные цели:", reply_markup=get_training_goals_keyboard())

@dp.message_handler(state=ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION_DETAILS)
async def process_physical_condition_details(message: types.Message, state: FSMContext):
    """Обработка пользовательского описания телосложения"""
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION.set()
        await message.answer("Как ты оцениваешь свою физическую форму?", reply_markup=get_physical_condition_keyboard())
        return
    
    custom_description = message.text.strip()
    await state.update_data(physical_condition=f"Свой вариант: {custom_description}")

    await ParticipantStates.WAITING_FOR_TRAINING_GOALS.set()
    await send_with_progress(message, state, "Тренировочные предпочтения и цели?", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выбери тренировочные цели:", reply_markup=get_training_goals_keyboard())


@dp.callback_query_handler(state=ParticipantStates.WAITING_FOR_TRAINING_GOALS)
async def process_training_goals(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка тренировочных целей из инлайн кнопок"""
    user = callback_query.from_user
    log_info(f"[TRAINING_GOALS] {user.id} | @{user.username} | {user.first_name} {user.last_name} | data: {callback_query.data}")

    data = callback_query.data
    await callback_query.answer()


    if data == "back":
        await ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION.set()
        await send_with_progress(callback_query.message, state, "Как ты оцениваешь свою физическую форму?", reply_markup=get_physical_condition_keyboard())
        return

    if data == "goal_other":
        await state.update_data(training_goals="Другие цели")
        await ParticipantStates.WAITING_FOR_TRAINING_GOALS_DETAILS.set()
        await callback_query.message.answer(
            "Опиши, пожалуйста, свою цель подробно:",
            reply_markup=get_back_keyboard()
        )
        return
    
    goals_mapping = {
        "goal_mass": "Хочу набрать мышечную массу",
        "goal_weight_loss": "Хочу сбросить вес",
        "goal_endurance": "Улучшить выносливость",
        "goal_strength": "Развить силу",
        "goal_maintenance": "Поддерживать общую физическую форму",
        "goal_bench_100": "Пожать 100 кг",
        "goal_kim_butt": "Хочу попу как у Ким",
        "goal_other": "Другие цели (с текстовым вводом для уточнения)",
    }

    if callback_query.data not in goals_mapping:
        await callback_query.answer("Выбор не распознан.")
        return

    goals = goals_mapping[callback_query.data]
    
    await state.update_data(training_goals=goals)

    await callback_query.message.edit_reply_markup()

    await callback_query.answer()
    await ParticipantStates.WAITING_FOR_MAIN_GOAL.set()
    await send_with_progress(callback_query.message, state,"Какова твоя главная цель?",reply_markup=get_back_keyboard())

@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRAINING_GOALS_DETAILS)
async def process_training_goals_details(message: types.Message, state: FSMContext):
    log_info(f"process_training_goals_details | message: {message.text}")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_GOALS.set()
        await message.answer(
            "Выбери тренировочные цели:",
            reply_markup=get_training_goals_keyboard()
        )
        return

    text = message.text.strip()
    if len(text) < 3:
        return await message.answer("Опиши, пожалуйста, более подробно цель.")

    await state.update_data(training_goals=text)
    await ParticipantStates.WAITING_FOR_MAIN_GOAL.set()
    await send_with_progress(
        message, state,
        "Какова твоя главная цель?",
        reply_markup=get_back_keyboard()
    )



@dp.message_handler(state=ParticipantStates.WAITING_FOR_MAIN_GOAL)
async def process_main_goal(message: types.Message, state: FSMContext):
    """Обработка главной цели"""
    log_user_input(message, label="MAIN_GOAL")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_GOALS.set()
        await message.answer("Тренировочные предпочтения и цели?", reply_markup=get_training_goals_keyboard())
        return

    main_goal = message.text.strip()
    await state.update_data(main_goal=main_goal)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_FITNESS_LEVEL.set()
    await send_with_progress(message, state, "Твой уровень физической подготовки?", reply_markup=get_fitness_level_keyboard())

@dp.message_handler(state=ParticipantStates.WAITING_FOR_FITNESS_LEVEL)
async def process_fitness_level(message: types.Message, state: FSMContext):
    """Обработка уровня физической подготовки"""
    log_user_input(message, label="FITNESS_LEVEL")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_MAIN_GOAL.set()
        await send_with_progress(message, state, "Какова твоя главная цель?", reply_markup=get_back_keyboard())
        return

    fitness_level = message.text.strip()

    if fitness_level not in ["Новичок", "Средний уровень", "Продвинутый", "Профессионал"]:
        await message.answer("Пожалуйста, выбери свой уровень физической подготовки из предложенных.")
        return

    await state.update_data(fitness_level=fitness_level)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_TRAINING_LOCATION.set()
    await send_with_progress(message, state, "Где ты предпочитаешь тренироваться?", reply_markup=get_training_location_keyboard())

# 9
@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRAINING_LOCATION)
async def process_training_location(message: types.Message, state: FSMContext):
    """Обработка предпочтений по месту тренировки"""
    log_user_input(message, label="TRAINING_LOCATION")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_FITNESS_LEVEL.set()
        await send_with_progress(message, state, "Твой уровень физической подготовки?", reply_markup=get_fitness_level_keyboard())
        return

    training_location = message.text.strip()

    valid_locations = ["В спортзале", "Дома", "На улице (парки, стадионы)", 
                      "В студии (йога, пилатес и т.п.)", "Могу тренироваться в любом месте"]
    
    if training_location not in valid_locations:
        await message.answer("Пожалуйста, выбери место тренировки из предложенных.")
        return

    await state.update_data(training_location=training_location)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_TRAINING_TIME.set()
    await send_with_progress(message, state, "Какое время суток тебе наиболее удобно для тренировок?", reply_markup=get_training_time_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRAINING_TIME)
async def process_training_time(message: types.Message, state: FSMContext):
    """Обработка времени суток для тренировок"""
    log_user_input(message, label="TRAINING_TIME")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_LOCATION.set()
        await send_with_progress(message, state, "Где ты предпочитаешь тренироваться?", reply_markup=get_training_location_keyboard())
        return

    training_time = message.text.strip()

    valid_times = ["Утром", "Днём", "Вечером", "Ночью"]
    
    if training_time not in valid_times:
        await message.answer("Пожалуйста, выбери время для тренировок из предложенных вариантов.")
        return

    await state.update_data(training_time=training_time)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_TRAINING_FREQUENCY.set() 
    await send_with_progress(message, state, "Сколько тренировок в неделю ты планируешь?", reply_markup=get_training_frequency_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRAINING_FREQUENCY)
async def process_training_frequency(message: types.Message, state: FSMContext):
    """Обработка количества тренировок в неделю"""
    log_user_input(message, label="TRAINING_FREQUENCY")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_TIME.set()
        await message.answer("Какое время суток тебе наиболее удобно для тренировок?", 
                           reply_markup=get_training_time_keyboard())
        return

    training_frequency = message.text.strip()

    valid_frequencies = ["2 дня", "3 дня", "4 дня", "5 дней"]
    
    if training_frequency not in valid_frequencies:
        await message.answer("Пожалуйста, выбери количество тренировок из предложенных вариантов.")
        return

    await state.update_data(training_frequency=training_frequency)
    await log_fsm_state(message, state)


    await ParticipantStates.WAITING_FOR_TRAINING_DURATION.set()
    await send_with_progress(message, state, "Какая длительность тренировок тебе подходит?", reply_markup=get_training_duration_keyboard())



@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRAINING_DURATION)
async def process_training_duration(message: types.Message, state: FSMContext):
    """Обработка длительности тренировок"""
    log_user_input(message, label="TRAINING_DURATION")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_FREQUENCY.set()
        await message.answer("Сколько тренировок в неделю ты планируешь?", 
                           reply_markup=get_training_frequency_keyboard())
        return

    training_duration = message.text.strip()

    valid_durations = ["До 30 минут", "30-45 минут", "45-60 минут", "Более 1 часа"]
    
    if training_duration not in valid_durations:
        await message.answer("Пожалуйста, выбери длительность тренировок из предложенных вариантов.")
        return

    await state.update_data(training_duration=training_duration)
    await log_fsm_state(message, state)

    user_data = await state.get_data()
    if not user_data.get("video_sent"):
        video_path = InputFile("bot/roundles/center.mp4")
        await message.answer_video_note(video_path)
        await state.update_data(video_sent=True)

        
    await ParticipantStates.WAITING_FOR_TRAINING_TYPES.set()
    await send_with_progress(message, state, "Какие виды тренировок ты предпочитаешь?", reply_markup=get_training_types_keyboard())

@dp.message_handler(state=ParticipantStates.WAITING_FOR_TRAINING_TYPES)
async def process_training_types(message: types.Message, state: FSMContext):
    """Обработка предпочитаемых видов тренировок"""
    log_user_input(message, label="TRAINING_TYPES")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_DURATION.set()
        await send_with_progress(message, state, "Какая длительность тренировок тебе подходит?", reply_markup=get_training_duration_keyboard())
        return

    training_types = message.text.strip()

    valid_types = [
        "Силовые тренировки (тяжёлая атлетика, тренажёры)",
        "Кардио (бег, велотренажёр, плавание)",
        "Круговые тренировки",
        "Функциональный тренинг",
        "Йога / Пилатес",
        "Спортивные игры (футбол, баскетбол и т.п.)",
        "Не знаю, готов пробовать разные виды"
    ]
    
    if training_types not in valid_types:
        await message.answer("Пожалуйста, выбери виды тренировок из предложенных вариантов.")
        return

    await state.update_data(training_types=training_types)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_LIMITATIONS.set()
    await send_with_progress(message, state, "Имеются ли ограничения или особенности (травмы, боли)?", reply_markup=get_limitations_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_LIMITATIONS)
async def process_limitations(message: types.Message, state: FSMContext):
    """Обработка наличия ограничений"""
    log_user_input(message, label="LIMITATIONS")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_TRAINING_TYPES.set()
        await send_with_progress(message, state, "Какие виды тренировок ты предпочитаешь?", reply_markup=get_training_types_keyboard())
        return

    limitations = message.text.strip()

    if limitations not in ["Да", "Нет"]:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(has_limitations=limitations)
    await log_fsm_state(message, state)

    if limitations == "Да":
        await ParticipantStates.WAITING_FOR_LIMITATIONS_DETAILS.set()
        await send_with_progress(message, state, "Опиши свои ограничения или особенности (травмы, боли):", reply_markup=get_back_keyboard())
    else:
        await ParticipantStates.WAITING_FOR_EATING_SCHEDULE.set()
        await send_with_progress(message, state, "Какой режим питания для тебя привычен?", reply_markup=get_eating_schedule_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_LIMITATIONS_DETAILS)
async def process_limitations_details(message: types.Message, state: FSMContext):
    """Обработка деталей ограничений"""
    log_user_input(message, label="LIMITATIONS_DETAILS")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_LIMITATIONS.set()
        await send_with_progress(message, state, "Имеются ли ограничения или особенности (травмы, боли)?", reply_markup=get_limitations_keyboard())
        return

    limitations_details = message.text.strip()
    
    if len(limitations_details) < 3:
        await message.answer("Пожалуйста, опиши подробнее свои ограничения или особенности.")
        return

    await state.update_data(limitations_details=limitations_details)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_EATING_SCHEDULE.set()
    await send_with_progress(message, state, "Какой режим питания для тебя привычен?", reply_markup=get_eating_schedule_keyboard())

