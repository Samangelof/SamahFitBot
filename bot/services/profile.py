from bot.settings.setup_bot import dp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ReplyKeyboardRemove
from bot.states.states import ParticipantStates
from bot.keyboards.keyboards import get_gender_keyboard, get_back_keyboard, get_physical_condition_keyboard
from bot.utils.debug_log import log_user_input, log_fsm_state
from bot.handlers.commands import start_command
from bot.utils.utils import send_with_progress


@dp.message_handler(state=ParticipantStates.WAITING_WELCOME)
async def process_welcome(message: types.Message, state: FSMContext):
    """Обработка нажатия кнопки 'Начать заполнение анкеты'"""
    if message.text != "Начать заполнение анкеты":
        await message.answer("Пожалуйста, нажмите кнопку ниже 👇, чтобы начать заполнение анкеты.")
        return

    await ParticipantStates.WAITING_FOR_NAME.set()
    await send_with_progress(message, state, "Как тебя зовут?", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_NAME)
async def process_name(message: types.Message, state: FSMContext):
    """Обработка имени"""
    # log_info(f"[NAME] от пользователя {message.from_user.id} | @{message.from_user.username} | текст: {message.text}")
    log_user_input(message, label="NAME")

    if message.text == "⬅️ Назад":
        await start_command(message, state)
        return
    
    name = message.text.strip()

    if not name.isalpha() or len(name) < 2:
        await message.answer("Пожалуйста, введи корректное имя без цифр и спецсимволов.")
        return
    
    if message.text.lower() in ["никто", "никак", "отмена", "нет"]:
        await message.answer(f"Уважаемый, введи свое корректное имя")
        return


    await state.update_data(name=name)
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_GENDER.set()
    await send_with_progress(message, state, "Укажи свой пол.", reply_markup=get_gender_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_GENDER)
async def process_gender(message: types.Message, state: FSMContext):
    """Обработка пола"""
    log_user_input(message, label="GENDER")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_NAME.set()
        await send_with_progress(message, state, "Как тебя зовут?", reply_markup=get_back_keyboard())
        return
    
    gender = message.text.strip().lower()

    if gender not in ["мужской", "женский", "м", "ж", "m", "w"]:
        await message.answer("Пожалуйста, выбери пол, используя кнопки ниже 👇.")
        return

    await state.update_data(gender=gender)
    await log_fsm_state(message, state)
    await ParticipantStates.WAITING_FOR_AGE.set()
    await send_with_progress(message, state, "Сколько тебе лет?", reply_markup=get_back_keyboard())


@dp.message_handler(state=ParticipantStates.WAITING_FOR_AGE)
async def process_age(message: types.Message, state: FSMContext):
    """Обработка возраста"""
    log_user_input(message, label="AGE")
    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_GENDER.set()
        await message.answer("Укажи свой пол.", reply_markup=get_gender_keyboard())
        return
    
    age_text = message.text.strip()
    if not age_text.isdigit() or not (10 <= int(age_text) <= 100):
        await message.answer("Пожалуйста, введи корректный возраст числом от 10 до 100 лет.")
        return

    await state.update_data(age=int(age_text))
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_HEIGHT.set()
    await send_with_progress(message, state, "Какой у тебя рост в сантиметрах?", reply_markup=get_back_keyboard())

@dp.message_handler(state=ParticipantStates.WAITING_FOR_HEIGHT)
async def process_height(message: types.Message, state: FSMContext):
    """Обработка роста"""
    log_user_input(message, label="HEIGHT")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_AGE.set()
        await message.answer("Сколько тебе лет?", reply_markup=get_back_keyboard())
        return
    
    height_text = message.text.strip()
    if not height_text.isdigit() or not (100 <= int(height_text) <= 250):
        await message.answer("Пожалуйста, введи корректный рост числом от 100 до 250 см.")
        return

    await state.update_data(height=int(height_text))
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_WEIGHT.set()
    await send_with_progress(message, state, "Какой у тебя вес в килограммах?", reply_markup=get_back_keyboard())
    
@dp.message_handler(state=ParticipantStates.WAITING_FOR_WEIGHT)
async def process_weight(message: types.Message, state: FSMContext):
    """Обработка веса"""
    log_user_input(message, label="WEIGHT")

    if message.text == "⬅️ Назад":
        await ParticipantStates.WAITING_FOR_HEIGHT.set()
        await message.answer("Какой у тебя рост в сантиметрах?", reply_markup=get_back_keyboard())
        return

    weight_text = message.text.strip()
    if not weight_text.isdigit() or int(weight_text) <= 0:
        await message.answer("Пожалуйста, введи корректный вес числом.")
        return

    if not weight_text.isdigit():
        await message.answer("Пожалуйста, введи вес числом (например, 75).")
        return

    weight = int(weight_text)
    if weight < 30 or weight > 300:
        await message.answer("Пожалуйста, введи реальный вес от 30 до 300 кг.")
        return
    
    await state.update_data(weight=int(weight_text))
    await log_fsm_state(message, state)

    await ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION.set()
    await send_with_progress(message, state, "Как ты оцениваешь свою физическую форму?", reply_markup=get_physical_condition_keyboard())