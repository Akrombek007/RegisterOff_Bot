from keyboards.inline import choose_education_status_info, choose_visitor
from aiogram.dispatcher import FSMContext
from file_service import get_file_path
from aiogram import types
from loader import dp
import os


@dp.callback_query_handler(text="information")
async def information(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(" <b>📘 Ta’lim shakllari va litsenziya haqida</b>\n\n",
                              reply_markup=choose_education_status_info)

