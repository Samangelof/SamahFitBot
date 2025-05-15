from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.states.states import ParticipantStates
from bot.states.states import QUESTION_NUMBERS, TOTAL_QUESTIONS
from bot.utils.logger import log_info, log_error, log_warning


async def send_with_progress(message: types.Message, state: FSMContext, text: str, reply_markup=None):
    current_state = await state.get_state()
    question_number = QUESTION_NUMBERS.get(current_state)

    if question_number:
        progress_text = f"({question_number}/{TOTAL_QUESTIONS}) {text}"
    else:
        progress_text = text

    await message.answer(progress_text, reply_markup=reply_markup)

# def format_application(user_data: dict) -> str:
#     fields = {
#         "Имя": "name",
#         "Пол": "gender",
#         "Возраст": "age",
#         "Рост": "height",
#         "Вес": "weight",
#         "Физическая форма": "physical_condition",
#         "Тренировочные цели": "training_goals",
#         "Главная цель": "main_goal",
#         "Уровень подготовки": "fitness_level",
#         "Место тренировок": "training_location",
#         "Время тренировок": "training_time",
#         "Частота тренировок": "training_frequency",
#         "Продолжительность тренировки": "training_duration",
#         "Типы тренировок": "training_types",
#         "Наличие ограничений": "has_limitations",
#         "График питания": "eating_schedule",
#         "Пищевые предпочтения": "diet_preferences",
#         "Аллергии": "has_allergies",
#         "Время на готовку": "cooking_time",
#         "Формат рецептов": "recipe_format",
#         "Ведение истории тренировок": "tracking_history",
#         "Приоритеты программы": "program_priority",
#         "Дополнительная информация": "additional_info",
#         "Опыт с спортивным питанием": "sports_nutrition_experience",
#         "Типы спортивного питания": "sports_nutrition_types",
#         "Бюджет на спортивное питание": "sports_nutrition_budget"
#     }


#     lines = ["Новая анкета! 🚀"]
#     for title, key in fields.items():
#         value = user_data.get(key, "Не указано")
#         lines.append(f"{title}: {value}")

#     return "\n".join(lines)





def format_application(answers: dict, user_first_name: str, user_username: str, application_id: int, amount: str) -> str:
    def get(key, suffix=''):
        val = answers.get(key)
        return f"{val}{suffix}" if val else "—"

    def get_bool(key):
        val = answers.get(key)
        if isinstance(val, str):
            val = val.lower()
        return "Ведётся" if val in ["да", "yes", "true", True] else "Нет"

    def get_list(key):
        val = answers.get(key)
        return ', '.join(val) if val else "—"

    # Форматируем анкету
    message = f"Новая анкета! 🚀\n\n"

    # Личные данные
    message += f"Имя: {get('name')}\n"
    message += f"Пол: {get('gender')}\n"
    message += f"Возраст: {get('age')}\n"
    message += f"Рост: {get('height')} см\n"
    message += f"Вес: {get('weight')} кг\n"
    message += f"Физическая форма: {get('physical_condition')}\n"
    message += f"Тренировочные цели: {get('training_goals')}\n"
    message += f"Главная цель: {get('main_goal')}\n"
    message += f"Уровень подготовки: {get('fitness_level')}\n"
    message += f"Место тренировок: {get('training_location')}\n"
    message += f"Время тренировок: {get('training_time')}\n"
    message += f"Частота тренировок: {get('training_frequency')} раз в неделю\n"
    message += f"Продолжительность тренировки: {get('training_duration')}\n"
    message += f"Типы тренировок: {get('training_types')}\n"
    message += f"Ограничения: {get('has_limitations')}\n\n"

    # Программа
    message += f"📦 Программа:\n"
    message += f"Формат рецептов: {get('recipe_format')}\n"
    message += f"История тренировок: {get_bool('tracking_history')}\n"
    message += f"Приоритеты программы: {get('program_priority')}\n\n"

    # Питание
    message += f"🥗 Питание:\n"
    message += f"График: {get('eating_schedule')}\n"
    message += f"Пищевые предпочтения: {get('diet_preferences')}\n"
    message += f"Аллергии: {get('has_allergies')}\n"
    message += f"Время на готовку: {get('cooking_time')}\n\n"

    # Спортивное питание
    message += f"💊 Спортивное питание:\n"
    message += f"Опыт: {get_bool('sports_nutrition_experience')}\n"
    message += f"Типы: {get_list('sports_nutrition_types')}\n"
    message += f"Бюджет: {get('sports_nutrition_budget')}\n\n"

    # Дополнительная информация
    message += f"Дополнительная информация: {get('additional_info')}\n\n"

    # Статус оплаты
    message += f"Статус оплаты: ✅ Оплачено\n"
    message += f"Сумма: {amount}₽\n"
    message += f"Telegram: @{user_username}\n"
    message += f"ID заявки: {application_id}\n"

    return message
