
from aiogram import Dispatcher
from bot.states.states import ParticipantStates
from bot.handlers.commands import start_command

from bot.services.profile import process_welcome, process_name, process_gender, process_age, process_height, process_weight

from bot.services.goals import process_physical_condition, process_training_goals, process_main_goal, \
    process_fitness_level, process_training_location,process_training_time, process_training_frequency,\
    process_training_duration, process_training_types, process_limitations, process_limitations_details

from bot.services.diet import process_eating_schedule, process_diet_preferences, process_diet_details, process_allergies, \
    process_allergies_details, process_cooking_time, process_recipe_format, process_recipe_format_details, process_tracking_history, process_program_priorities, \
    process_additional_info

from bot.services.supplements import (
    process_sports_nutrition_experience,
    process_sports_nutrition_types,
    process_sports_nutrition_budget
)

from bot.handlers.chat import handle_text_message


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"], state="*")
    dp.register_message_handler(process_welcome, state=ParticipantStates.WAITING_WELCOME) 
    dp.register_message_handler(process_name, state=ParticipantStates.WAITING_FOR_NAME) # 1
    dp.register_message_handler(process_gender, state=ParticipantStates.WAITING_FOR_GENDER)
    dp.register_message_handler(process_age, state=ParticipantStates.WAITING_FOR_AGE)
    dp.register_message_handler(process_height, state=ParticipantStates.WAITING_FOR_HEIGHT)
    dp.register_message_handler(process_weight, state=ParticipantStates.WAITING_FOR_WEIGHT)
    dp.register_message_handler(process_physical_condition, state=ParticipantStates.WAITING_FOR_PHYSICAL_CONDITION)
    dp.register_message_handler(process_training_goals, state=ParticipantStates.WAITING_FOR_TRAINING_GOALS)
    dp.register_message_handler(process_main_goal, state=ParticipantStates.WAITING_FOR_MAIN_GOAL)
    dp.register_message_handler(process_fitness_level, state=ParticipantStates.WAITING_FOR_FITNESS_LEVEL)
    dp.register_message_handler(process_training_location, state=ParticipantStates.WAITING_FOR_TRAINING_LOCATION)
    dp.register_message_handler(process_training_time, state=ParticipantStates.WAITING_FOR_TRAINING_TIME)
    dp.register_message_handler(process_training_frequency, state=ParticipantStates.WAITING_FOR_TRAINING_FREQUENCY)
    dp.register_message_handler(process_training_duration, state=ParticipantStates.WAITING_FOR_TRAINING_DURATION)
    dp.register_message_handler(process_training_types, state=ParticipantStates.WAITING_FOR_TRAINING_TYPES)
    dp.register_message_handler(process_limitations, state=ParticipantStates.WAITING_FOR_LIMITATIONS) # 15
    dp.register_message_handler(process_limitations_details, state=ParticipantStates.WAITING_FOR_LIMITATIONS_DETAILS) # 16
    dp.register_message_handler(process_eating_schedule, state=ParticipantStates.WAITING_FOR_EATING_SCHEDULE)   # 17
    dp.register_message_handler(process_diet_preferences, state=ParticipantStates.WAITING_FOR_DIET_PREFERENCES)
    dp.register_message_handler(process_diet_details, state=ParticipantStates.WAITING_FOR_DIET_DETAILS)
    dp.register_message_handler(process_allergies, state=ParticipantStates.WAITING_FOR_ALLERGIES)
    dp.register_message_handler(process_allergies_details, state=ParticipantStates.WAITING_FOR_ALLERGIES_DETAILS)
    dp.register_message_handler(process_cooking_time, state=ParticipantStates.WAITING_FOR_COOKING_TIME)
    dp.register_message_handler(process_recipe_format, state=ParticipantStates.WAITING_FOR_RECIPE_FORMAT)
    dp.register_message_handler(process_recipe_format_details, state=ParticipantStates.WAITING_FOR_RECIPE_FORMAT_DETAILS)
    dp.register_message_handler(process_tracking_history, state=ParticipantStates.WAITING_FOR_TRACKING_HISTORY)
    dp.register_message_handler(process_program_priorities, state=ParticipantStates.WAITING_FOR_PROGRAM_PRIORITIES)
    dp.register_message_handler(process_additional_info, state=ParticipantStates.WAITING_FOR_ADDITIONAL_INFO)
    dp.register_message_handler(process_sports_nutrition_experience, state=ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE)
    dp.register_message_handler(process_sports_nutrition_types, state=ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_TYPES)
    dp.register_message_handler(process_sports_nutrition_budget, state=ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_BUDGET)
    
    dp.register_message_handler(handle_text_message, state=None)