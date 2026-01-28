from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import asyncio
from core.db_settings import execute_query
from core.models import users
from core.config import BOT_TOKEN
from aiogram.fsm.state import StatesGroup, State


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


class UserState(StatesGroup):
    username = State()
    phone_number = State()
    age = State()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Enter your username:")
    await state.set_state(UserState.username)

@router.message(UserState.username)
async def get_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Enter your phone number (without '+'):")
    await state.set_state(UserState.phone_number)

@router.message(UserState.phone_number)
async def get_phone(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("do not include '+' in your number! Try again: ")
        return

    await state.update_data(phone_number=int(message.text))
    await message.answer("Enter your age: ")
    await state.set_state(UserState.age)

from core.db_settings import execute_query

@router.message(UserState.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Age must include only numbers! Try again:")
        return

    data = await state.get_data()

    query = """
        INSERT INTO users (username, phone_number, age)
        VALUES (%s, %s, %s)
    """

    result = execute_query(
        query=query,
        params=(
            data["username"],
            data["phone_number"],
            int(message.text)
        )
    )

    if result:
        await message.answer("✅ User successfully registered")
    else:
        await message.answer("❌ Unexpected troubles, try again")

    await state.clear()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, polling_timeout=0)
    
if __name__ == "__main__":
    # execute_query(users)
    asyncio.run(main())