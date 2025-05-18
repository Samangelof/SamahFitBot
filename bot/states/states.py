from aiogram.dispatcher.filters.state import State, StatesGroup


class ParticipantStates(StatesGroup):
    """Состояния для конечного автомата регистрации участника"""
    WAITING_WELCOME = State()  # Ожидание приветствия
    WAITING_FOR_NAME = State()  # Ожидание имени
    WAITING_FOR_GENDER = State()  # Ожидание гендера
    WAITING_FOR_AGE = State()  # Ожидание возраста
    WAITING_FOR_HEIGHT = State()  # Ожидание роста
    WAITING_FOR_WEIGHT = State()  # Ожидание веса
    WAITING_FOR_PHYSICAL_CONDITION = State()  # Ожидание физической формы
    WAITING_FOR_PHYSICAL_CONDITION_DETAILS = State()
    WAITING_FOR_TRAINING_GOALS = State()  # Ожидание целей тренировки
    WAITING_FOR_TRAINING_GOALS_DETAILS = State()
    WAITING_FOR_MAIN_GOAL = State()  # Ожидание главной цели
    WAITING_FOR_FITNESS_LEVEL = State()  # Ожидание уровня физической подготовки
    WAITING_FOR_TRAINING_LOCATION = State()  # Ожидание места тренировки
    WAITING_FOR_TRAINING_TIME = State()  # Ожидание времени суток для тренировок
    WAITING_FOR_TRAINING_FREQUENCY = State()  # Ожидание количества тренировок в неделю
    WAITING_FOR_TRAINING_DURATION = State()  # Ожидание длительности тренировок
    WAITING_FOR_TRAINING_TYPES = State()  # Ожидание предпочитаемых видов тренировок
    WAITING_FOR_LIMITATIONS = State()  # Ожидание информации об ограничениях/травмах
    WAITING_FOR_LIMITATIONS_DETAILS = State()  # Ожидание деталей об ограничениях, если есть
    WAITING_FOR_EATING_SCHEDULE = State()  # Ожидание режима питания
    WAITING_FOR_EATING_SCHEDULE_DETAIL = State()
    WAITING_FOR_DIET_PREFERENCES = State()  # Ожидание диетических предпочтений
    WAITING_FOR_DIET_DETAILS = State()  # Ожидание деталей диетических предпочтений, если "Другие"
    WAITING_FOR_ALLERGIES = State()  # Ожидание информации об аллергиях
    WAITING_FOR_ALLERGIES_DETAILS = State()  # Ожидание деталей об аллергиях, если есть
    WAITING_FOR_COOKING_TIME = State()  # Ожидание времени на приготовление еды
    WAITING_FOR_RECIPE_FORMAT = State()  # Ожидание предпочитаемого формата рецептов
    WAITING_FOR_RECIPE_FORMAT_DETAILS = State()  # Ожидание деталей формата рецептов, если "Другой формат"
    WAITING_FOR_TRACKING_HISTORY = State()
    WAITING_FOR_PROGRAM_PRIORITIES = State()
    WAITING_FOR_ADDITIONAL_INFO = State()
    WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE = State()
    WAITING_FOR_SPORTS_NUTRITION_TYPES = State()
    WAITING_FOR_SPORTS_NUTRITION_BUDGET = State()
    
    WAITING_FOR_CODE = State()
    WAITING_FOR_PERCENT = State()

    COMPLETED = State()


TOTAL_QUESTIONS = 26

QUESTION_NUMBERS = {
    ParticipantStates.WAITING_FOR_NAME.state: 1,
    ParticipantStates.WAITING_FOR_GENDER.state: 2,
    ParticipantStates.WAITING_FOR_AGE.state: 3,
    ParticipantStates.WAITING_FOR_HEIGHT.state: 4,
    ParticipantStates.WAITING_FOR_WEIGHT.state: 5,
    ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION.state: 6,
    ParticipantStates.WAITING_FOR_TRAINING_GOALS.state: 7,
    ParticipantStates.WAITING_FOR_MAIN_GOAL.state: 8,
    ParticipantStates.WAITING_FOR_FITNESS_LEVEL.state: 9,
    ParticipantStates.WAITING_FOR_TRAINING_LOCATION.state: 10,
    ParticipantStates.WAITING_FOR_TRAINING_TIME.state: 11,
    ParticipantStates.WAITING_FOR_TRAINING_FREQUENCY.state: 12,
    ParticipantStates.WAITING_FOR_TRAINING_DURATION.state: 13,
    ParticipantStates.WAITING_FOR_TRAINING_TYPES.state: 14,
    ParticipantStates.WAITING_FOR_LIMITATIONS.state: 15,
    ParticipantStates.WAITING_FOR_EATING_SCHEDULE.state: 16,
    ParticipantStates.WAITING_FOR_DIET_PREFERENCES.state: 17,
    ParticipantStates.WAITING_FOR_ALLERGIES.state: 18,
    ParticipantStates.WAITING_FOR_COOKING_TIME.state: 19,
    ParticipantStates.WAITING_FOR_RECIPE_FORMAT.state: 20,
    ParticipantStates.WAITING_FOR_TRACKING_HISTORY.state: 21,
    ParticipantStates.WAITING_FOR_PROGRAM_PRIORITIES.state: 22,
    ParticipantStates.WAITING_FOR_ADDITIONAL_INFO.state: 23,
    ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE.state: 24,
    ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_TYPES.state: 25,
    ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_BUDGET.state: 26,
}
