from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from loguru import logger

from app.bot.handlers.callbackdata import StartCb, AdminCb, GoToCb
from app.bot.handlers.keyboards.admin import admin_menu_keyboard, admin_mailing_submit_keyboard, \
    admin_mailing_select_language_keyboard
from app.bot.handlers.states.admin import AdminState
from app.core.constants import DATE_FORMAT, get_files_dir
from app.utils.excel.export import get_excel_user
from app.utils.mailing import send_mailing_all

admin_router = Router()


@admin_router.callback_query(StartCb.filter(F.action == 'admin'))
async def start_admin_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    await call.message.answer(text=_("messages.admin"), reply_markup=admin_menu_keyboard(_))


# @admin_router.callback_query(AdminState)
@admin_router.callback_query(GoToCb.filter(F.action == 'admin'))
async def go_to_admin_handler(call: CallbackQuery, state: FSMContext, _):
    await start_admin_handler(call, state, _)


"""Export"""


@admin_router.callback_query(AdminCb.filter(F.action == 'export_users'))
async def admin_export_users_handler(call: CallbackQuery, state: FSMContext, _):
    if await get_excel_user():
        date = datetime.now().strftime(DATE_FORMAT)
        await call.message.answer_document(document=FSInputFile(f"{get_files_dir()}/USERS_{date}.xlsx"),
                                           caption=_("messages.admin_export_users_confirm"))
    else:
        logger.info("ОШИБКА ВЫГРУЗКИ ФАЙЛА")
    await start_admin_handler(call, state, _)


"""Do mailing"""


@admin_router.callback_query(AdminCb.filter(F.action == 'mailing'))
async def admin_mailing_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    await call.message.answer(text=_("messages.admin_mailing_language"),
                              reply_markup=admin_mailing_select_language_keyboard(_))


@admin_router.callback_query(AdminCb.filter(F.action == 'mailing_language_ru'))
@admin_router.callback_query(AdminCb.filter(F.action == 'mailing_language_en'))
async def admin_mailing_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    call_data = AdminCb.unpack(call.data)
    await state.update_data(language=call_data.action.split('_')[-1])
    await call.message.answer(text=_("messages.admin_mailing_text"))
    await state.set_state(AdminState.mailing_text)


@admin_router.message(AdminState.mailing_text)
async def admin_mailing_text_handler(message: Message, state: FSMContext, _):
    state_data = await state.get_data()
    if message.text:
        await state.update_data(text=message.text)
        await message.answer(text=_("messages.admin_mailing_submit",
                                    language=_(f"buttons.{state_data['language']}"),
                                    send_message=message.text),
                             reply_markup=admin_mailing_submit_keyboard(_))
    else:
        logger.info(message.caption)
        await state.update_data(text=message.caption)
        if message.photo:
            await state.update_data(photo_id=message.photo[-1].file_id)
            await message.answer_photo(caption=_("messages.admin_mailing_submit",
                                                 language=_(f"buttons.{state_data['language']}"),
                                                 send_message=message.caption),
                                       photo=message.photo[-1].file_id,
                                       reply_markup=admin_mailing_submit_keyboard(_))
        elif message.video:
            await state.update_data(video_id=message.video.file_id)
            await message.answer_video(caption=_("messages.admin_mailing_submit",
                                                 language=_(f"buttons.{state_data['language']}"),
                                                 send_message=message.caption),
                                       video=message.video.file_id,
                                       reply_markup=admin_mailing_submit_keyboard(_))
        elif message.document:
            await state.update_data(document_id=message.document.file_id)
            await message.answer_document(caption=_("messages.admin_mailing_submit",
                                                    language=_(f"buttons.{state_data['language']}"),
                                                    send_message=message.caption),
                                          document=message.document.file_id,
                                          reply_markup=admin_mailing_submit_keyboard(_))
    await state.set_state(AdminState.mailing_submit)


@admin_router.callback_query(AdminState.mailing_submit, AdminCb.filter(F.action == 'mailing_yes'))
async def admin_mailing_handler(call: CallbackQuery, state: FSMContext, _):
    await call.message.delete()
    state_data = await state.get_data()
    mailing_info = await send_mailing_all(text=state_data.get("text"), language=state_data["language"],
                                          photo_id=state_data.get("photo_id"), video_id=state_data.get("video_id"),
                                          document_id=state_data.get("document_id"))
    await call.message.answer(text=_("messages.admin_mailing_confirm",
                                     count_users=mailing_info[0], all_users=mailing_info[1]))
    await state.clear()
