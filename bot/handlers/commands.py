from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from bot.settings.setup_bot import dp, db
from bot.states.states import ParticipantStates
from bot.utils.logger import log_info, log_warning
from bot.keyboards.keyboards import get_start_keyboard
from bot.utils.excel_export import export_to_excel
from bot.settings.config import ADMIN_IDS, TELEGRAM_BOT_USERNAME
from bot.settings.setup_bot import db
from bot.database.crud import user as user_crud
from bot.database.crud import visits as visit_crud
from bot.database.crud import applications as application_crud
from bot.database.crud import visits as visit_crud
from bot.database.crud import referral as referral_crud


# # ! DEBUG [HACK] - убрать на проде
# @dp.message_handler(commands=["start"], state="*")
# async def start_command_debug_hack(message: types.Message, state: FSMContext):
#     """[HACK] Принудительно переходит к нужному состоянию для теста"""
#     await state.set_state(ParticipantStates.WAITING_FOR_SPORTS_NUTRITION_EXPERIENCE)

#     log_info(f'[HACK] message.from_user: {message.from_user}')

#     with db.session_scope() as session:
#         user_crud.get_or_create(session, message.from_user)
#         visit_crud.log_visit(session, message.from_user)

#         args = message.get_args()
#         if args.isdigit():
#             inviter_telegram_id = int(args)
#             if inviter_telegram_id != message.from_user.id:
#                 referral_crud.add_referral(session, inviter_telegram_id, message.from_user.id)
#                 log_info(f"[HACK] User {message.from_user.id} был приглашен пользователем {inviter_telegram_id}")
#             else:
#                 log_info("[HACK] Пользователь попытался пригласить сам себя — пропускаем")

#     await message.answer(
#         "Привет! Готов помочь тебе составить персональную программу тренировок и питания 💪\n\n"
#     )

#     await process_sports_nutrition_experience(message, state)





@dp.message_handler(commands=["start"], state="*")
async def start_command(message: types.Message, state: FSMContext):
    log_info(f"start_command | message: {message.text}")
    await state.finish()
    log_info(f'message.from_user: {message.from_user}')

    with db.session_scope() as session:
        user_crud.get_or_create(session, message.from_user)
        visit_crud.log_visit(session, message.from_user)

        args = message.get_args()
        if args.isdigit():
            inviter_telegram_id = int(args)
            if inviter_telegram_id != message.from_user.id:
                referral_crud.add_referral(session, inviter_telegram_id, message.from_user.id)
                log_info(f"User {message.from_user.id} был приглашен пользователем {inviter_telegram_id}")
            else:
                log_info("Пользователь попытался пригласить сам себя — пропускаем")

    await message.answer(
        "Привет! Готов помочь тебе составить персональную программу тренировок и питания 💪\n\n"
    )

    video_path = InputFile("bot/roundles/start.mp4")
    await message.answer_video_note(video_path)

    await message.answer("Давай начнем! 👇", reply_markup=get_start_keyboard())
    await ParticipantStates.WAITING_WELCOME.set()




@dp.message_handler(commands=['status'], state="*")
async def check_payment_status_command(message: types.Message):
    """Обработчик команды для проверки статуса оплаты (антиспам!)"""
    log_info(f"check_payment_status_command | from user {message.from_user.id}")

    with db.session_scope() as session:
        applications = application_crud.get_user_applications(session, message.from_user.id)

    if not applications:
        await message.answer("У тебя еще нет заявок. Чтобы создать заявку, нажми /start")
        return

    latest_app = applications[0]

    if latest_app['payment_status'] == 'оплачено':
        await message.answer(
            "✅ Твоя последняя заявка оплачена!\n\n"
        )
        await message.answer(
            "Спасибо за оплату!\n"
            "Ты сделал(а) первый шаг к своей новой форме!\n"
            "Готовимся менять жизнь!\n\n"
            "⚙️ Сейчас я анализирую твои ответы и подбираю персональную программу тренировок и питания.\n"
            "Все делаю вручную, с душой и вниманием к деталям — никакого копипаста!\n\n"
            "⏳ Ожидай PDF-документ в течение 1–2 рабочих дней — там будет всё:\n"
            "что есть 🍽️, как тренироваться 🏋️‍♀️, когда отдыхать 💤 и как уверенно идти к цели!\n\n"
            "Если что-то захочешь уточнить — пиши, я всегда на связи!\n\n"
            "Скоро начнём!\n"
            "🔥 #ТвойПутьНачался"
        )
        return

    # Если заявка не оплачена, работаем с payment_id/payment_url
    payment_id = latest_app.get('payment_id')
    payment_url = latest_app.get('payment_url')  # добавь это поле в БД и сохраняй при генерации ссылки

    if payment_id and payment_url:
        # Если уже есть активная ссылка — просто повторно отправляем её, не создаём новую!
        await message.answer(
            "🔄 Твоя заявка еще не оплачена.\n\n"
            "Для оплаты используй кнопку ниже:",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Оплатить заявку", url=payment_url)
            )
        )
    else:
        # Генерируем новую ссылку только если её ещё нет
        from bot.services.payment_service import generate_payment_link
        await generate_payment_link(message, None, latest_app['id'])




@dp.message_handler(commands=["promocode"], state="*")
async def ask_promocode(message: types.Message, state: FSMContext):
    await message.answer("Введи промокод, если есть:")
    await state.set_state("waiting_for_promocode")

@dp.message_handler(state="waiting_for_promocode")
async def process_promocode(message: types.Message, state: FSMContext):
    code = message.text.strip()
    promocode = db.get_promocode(code)
    if promocode and promocode[1]:
        discount = promocode[0]
        await state.update_data(promocode=code.upper(), promocode_discount=discount)
        await message.answer(f"Промокод принят! Скидка {discount}%")
    else:
        await message.answer("Такого промокода нет или он не активен. Попробуй ещё раз.")
    await state.finish()


@dp.message_handler(commands=["my_discount"], state="*")
async def my_discount_command(message: types.Message):
    telegram_id = message.from_user.id
    discount_percent = db.get_discount_percent(telegram_id)
    
    await message.answer(f"Твоя текущая скидка: {discount_percent}%.\n\n"
                         "Приводи друзей и увеличивай скидку до 50%!")


@dp.message_handler(commands=["my_referral_link"], state="*")
async def my_referral_link_command(message: types.Message):
    telegram_id = message.from_user.id
    referral_link = f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={telegram_id}"
    
    await message.answer(f"Вот твоя персональная реферальная ссылка:\n\n{referral_link}\n\n"
                         "Отправляй её друзьям, чтобы получать скидку за каждого приглашённого 💪")



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('pay_'))
async def process_payment_button(callback_query: types.CallbackQuery):
    """Обработчик кнопки оплаты"""
    await callback_query.answer()
    log_info(f"process_payment_button | from user {callback_query.from_user.id}")
    
    app_id = int(callback_query.data.split('_')[1])
    
    from bot.services.payment_service import generate_payment_link
    await generate_payment_link(callback_query.message, None, app_id)


@dp.message_handler(commands=['get_data'], state="*")
async def get_data_command(message: types.Message):
    """Выгрузка Excel с заявками (доступно только админам)"""
    if message.from_user.id not in ADMIN_IDS:
        log_warning(f"Попытка неадмина {message.from_user.id} вызвать /get_data")
        await message.answer("У тебя нет прав для этой команды.")
        return

    log_info(f"get_data_command | админ {message.from_user.id} запросил данные")

    db_path = "bot_database.db"
    excel_path = "export.xlsx"
    export_to_excel(db_path, excel_path)

    await message.answer_document(InputFile(excel_path), caption="Вот твои данные 📊")


@dp.message_handler(commands=['stats'], state="*")
async def bot_stats(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У тебя нет доступа к этой команде.")
        return

    visits = db.get_daily_visits()

    if not visits:
        await message.answer("Нет данных по активности.")
        return

    text = "📊 Активность за последние 30 дней:\n\n"
    for date, count in visits:
        text += f"📅 {date}: {count} визитов\n"

    unique_users = db.get_unique_user_count()
    text += f"\n👥 Уникальных пользователей всего: {unique_users}"

    await message.answer(text)
