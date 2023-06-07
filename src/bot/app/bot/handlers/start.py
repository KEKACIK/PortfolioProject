from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app import repo
from app.bot.handlers.callbackdata.start import GoToCb
from app.bot.handlers.keyboards.start import start_menu_keyboard
from app.misc import bot

start_router = Router()


@start_router.message(Command("start"))
async def start_menu_handler(message: Message, state: FSMContext, _):
    bot_name = (await bot.get_me()).full_name
    user = await repo.users.get(message.chat.id)
    await message.answer(text=_("messages.start", bot_name=bot_name),
                         reply_markup=start_menu_keyboard(_, is_admin=user.is_admin))


@start_router.callback_query(GoToCb.filter(F.action == 'start'))
async def go_to_start_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    await start_menu_handler(call.message, state, _)
