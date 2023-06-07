from typing import Callable, Dict, Any, Awaitable
from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram.types import Update

from app import repo
from app.misc import dp, locale_manager


async def update_user(update: Union[Message, CallbackQuery]):
    user = await repo.users.get(update.from_user.id)
    update_data = {}
    if user:
        if user.username != update.from_user.username:
            update_data["username"] = update.from_user.username
        if user.fullname != update.from_user.full_name:
            update_data["fullname"] = update.from_user.full_name
        if update_data:
            await repo.users.update(db_obj=user, **update_data)
    else:
        user = await repo.users.create(id=update.from_user.id,
                                       username=update.from_user.username, fullname=update.from_user.full_name)
    return user


@dp.update.outer_middleware()
async def BigBro(handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], event: Update,
                 data: Dict[str, Any]) -> Any:
    user = await update_user(event.message or event.callback_query)
    if user.locale:
        data["_"] = locale_manager.get_locale(user.locale).get
    else:
        data["_"] = locale_manager.get_locale("en").get

    return await handler(event, data)
