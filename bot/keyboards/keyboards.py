from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton, 
    ReplyKeyboardMarkup
)


def get_start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Начать заполнение анкеты", callback_data="start_form"))
    return keyboard


def get_back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("⬅️ Назад")]],
        resize_keyboard=True
    )

def get_physical_condition_keyboard():
    """Клавиатура для вопроса о физическом состоянии"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Худое телосложение"))
    keyboard.add(KeyboardButton("Спортивного телосложения"))
    keyboard.add(KeyboardButton("Имею лишние кг"))
    keyboard.add(KeyboardButton("Свой вариант"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_gender_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Мужской"), KeyboardButton("Женский")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )


def get_training_goals_keyboard():
    """Инлайн клавиатура для выбора целей тренировки"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Хочу набрать мышечную массу", callback_data="goal_mass"),
        InlineKeyboardButton("Хочу сбросить вес", callback_data="goal_weight_loss"),
        InlineKeyboardButton("Улучшить выносливость", callback_data="goal_endurance"),
        InlineKeyboardButton("Развить силу", callback_data="goal_strength"),
        InlineKeyboardButton("Поддерживать общую физическую форму", callback_data="goal_maintenance"),
        InlineKeyboardButton("Пожать 100 кг", callback_data="goal_bench_100"),
        InlineKeyboardButton("Хочу попу как у Ким", callback_data="goal_kim_butt"),
        InlineKeyboardButton("Другие цели (с текстовым вводом для уточнения)", callback_data="goal_other"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back")
    ]
    keyboard.add(*buttons)
    return keyboard

def get_fitness_level_keyboard():
    """Клавиатура для выбора уровня физической подготовки"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("Новичок"),
        KeyboardButton("Средний уровень"),
        KeyboardButton("Продвинутый"),
        KeyboardButton("Профессионал"),
        KeyboardButton("⬅️ Назад")
    ]
    keyboard.add(*buttons)
    return keyboard

def get_training_location_keyboard():
    """Клавиатура для выбора места тренировки"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("В спортзале"),
        KeyboardButton("Дома"),
        KeyboardButton("На улице (парки, стадионы)"),
        KeyboardButton("В студии (йога, пилатес и т.п.)"),
        KeyboardButton("Могу тренироваться в любом месте"),
        KeyboardButton("⬅️ Назад")
    ]
    for button in buttons:
        keyboard.add(button)
    return keyboard

def get_training_time_keyboard():
    """Клавиатура для выбора времени суток для тренировок"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Утром")],
            [KeyboardButton("Днём")],
            [KeyboardButton("Вечером")],
            [KeyboardButton("Ночью")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_training_frequency_keyboard():
    """Клавиатура для выбора количества тренировок в неделю"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("2 дня")],
            [KeyboardButton("3 дня")],
            [KeyboardButton("4 дня")],
            [KeyboardButton("5 дней")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_training_duration_keyboard():
    """Клавиатура для выбора длительности тренировок"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("До 30 минут")],
            [KeyboardButton("30-45 минут")],
            [KeyboardButton("45-60 минут")],
            [KeyboardButton("Более 1 часа")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_training_types_keyboard():
    """Клавиатура для выбора предпочитаемых видов тренировок"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("Силовые тренировки (тяжёлая атлетика, тренажёры)"),
        KeyboardButton("Кардио (бег, велотренажёр, плавание)"),
        KeyboardButton("Круговые тренировки"),
        KeyboardButton("Функциональный тренинг"),
        KeyboardButton("Йога / Пилатес"),
        KeyboardButton("Спортивные игры (футбол, баскетбол и т.п.)"),
        KeyboardButton("Не знаю, готов пробовать разные виды"),
        KeyboardButton("⬅️ Назад")
    ]
    for button in buttons:
        keyboard.add(button)
    return keyboard

def get_limitations_keyboard():
    """Клавиатура для выбора наличия ограничений"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Нет")],
            [KeyboardButton("Да")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_eating_schedule_keyboard():
    """Клавиатура для выбора режима питания"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Трехразовое питание")],
            [KeyboardButton("Пятиразовое питание")],
            [KeyboardButton("Частые перекусы")],
            [KeyboardButton("Другой режим")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_diet_preferences_keyboard():
    """Клавиатура для выбора диетических предпочтений"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("Без ограничений"),
        KeyboardButton("Вегетарианство"),
        KeyboardButton("Веганство"),
        KeyboardButton("Без глютена"),
        KeyboardButton("Без молочных продуктов"),
        KeyboardButton("Другие"),
        KeyboardButton("⬅️ Назад")
    ]
    for button in buttons:
        keyboard.add(button)
    return keyboard

def get_allergies_keyboard():
    """Клавиатура для выбора наличия аллергий"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Нет")],
            [KeyboardButton("Да")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_cooking_time_keyboard():
    """Клавиатура для выбора времени на приготовление еды"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("До 15 минут")],
            [KeyboardButton("15-30 минут")],
            [KeyboardButton("30-45 минут")],
            [KeyboardButton("Более 45 минут")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def get_recipe_format_keyboard():
    """Клавиатура для выбора формата рецептов"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Пошаговые рецепты с фото"))
    keyboard.add(KeyboardButton("Простой список ингредиентов и инструкции"))
    keyboard.add(KeyboardButton("Видеорецепты"))
    keyboard.add(KeyboardButton("Другой формат"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_tracking_history_keyboard():
    """Клавиатура для вопроса о ведении истории изменений"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_program_priorities_keyboard():
    """Клавиатура для выбора приоритетов в программе"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Простота и понятность"))
    keyboard.add(KeyboardButton("Результативность и быстрые изменения"))
    keyboard.add(KeyboardButton("Гибкость (можно менять программу в зависимости от ситуации)"))
    keyboard.add(KeyboardButton("Баланс между тренировками и питанием"))
    keyboard.add(KeyboardButton("Доступность (необходимые продукты и тренировки)"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_additional_info_keyboard():
    """Клавиатура для дополнительной информации"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    # Тут можно добавить какие-то часто задаваемые вопросы или оставить только кнопку "Назад"
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_sports_nutrition_experience_keyboard():
    """Клавиатура для вопроса об опыте использования спортивного питания"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_sports_nutrition_types_keyboard():
    """Клавиатура для выбора типов спортивного питания"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Протеины"))
    keyboard.add(KeyboardButton("Креатин"))
    keyboard.add(KeyboardButton("BCAA"))
    keyboard.add(KeyboardButton("Гейнеры"))
    keyboard.add(KeyboardButton("Жиросжигатели"))
    keyboard.add(KeyboardButton("Другие добавки"))
    keyboard.add(KeyboardButton("Далее"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard

def get_sports_nutrition_types_skip_keyboard():
    """Клавиатура с Пропустить и Назад, если пользователь не пробовал спортпит"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Пропустить"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard


def get_sports_nutrition_budget_keyboard():
    """Клавиатура для вопроса о бюджете на спортивное питание"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(KeyboardButton("Да, без проблем"))
    keyboard.add(KeyboardButton("Иногда могу позволить себе"))
    keyboard.add(KeyboardButton("Нет, это слишком дорого"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    return keyboard