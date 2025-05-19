from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from bot.utils.logger import log_info


def log_user_input(message: Message, label: str = "INPUT"):
    user = message.from_user
    log_info(
        f"[{label}] {user.id} | @{user.username} | {user.first_name} {user.last_name} | text: {message.text}"
    )


async def log_fsm_state(message: Message, state: FSMContext):
    data = await state.get_data()
    log_info(f"[FSM] {message.from_user.id} | data: {data}")