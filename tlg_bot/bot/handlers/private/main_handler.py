from random import randint

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from apps.models import User

main_router = Router()


class Form(StatesGroup):
    phone_number = State()
    username = State()
    password = State()


@main_router.message(F.text == "/login")
async def login_handler(message: Message):
    if cache.get(message.from_user.id):
        await message.answer("Eski kodingiz hali ham kuchda ☝️")
    else:
        ikb = InlineKeyboardBuilder()
        ikb.row(InlineKeyboardButton(text="🔄 Kodni yangilash", callback_data='refresh'))
        conf_code = randint(10000, 99999)
        cache.set(message.from_user.id, str(conf_code), 20)
        await message.answer(f"🔒 Kodingiz: {conf_code}", reply_markup=ikb.as_markup())


@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text='☎️ Kontaktni Yuborish', request_contact=True))
    await state.set_state(Form.phone_number)
    await message.answer(
        f"Salom, {hbold(message.from_user.full_name)}! 👋 \n\n⬇ Kontaktingizni yuboring (tugmani bosib)",
        reply_markup=kb.as_markup(resize_keybaord=True))


@main_router.message(Form.phone_number)
async def phone_number_handler(message: Message, state: FSMContext) -> None:
    try:
        phone_number = message.contact.phone_number
    except AttributeError as e:
        await message.answer('⬇ Kontaktingizni yuboring (tugmani bosib)')
        return

    await state.update_data(phone_number=phone_number)
    await state.set_state(Form.username)
    rm = ReplyKeyboardRemove()
    conf_code = randint(10000, 99999)
    await message.answer(f"Ixtiyoriy username kiritig: ", reply_markup=rm)


@main_router.message(Form.username)
async def username_handler(message: Message, state: FSMContext) -> None:
    if len(message.text) >= 3:
        try:
            user = await User.objects.aget(username=message.text)
            await message.answer('Bunday username mavjud boshqa username kiriting! ')
            return
        except ObjectDoesNotExist as e:
            await state.update_data(username=message.text)
            await state.set_state(Form.password)
    else:
        await message.answer("username kamidata 3 belgi bo'lishi mumkin: ")
        return

    await message.answer("pasword yarating: ")


@main_router.message(Form.password)
async def username_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    conf_code = randint(10000, 99999)
    data = await state.get_data()
    await state.clear()
    await message.answer(f"🔒 Kodingiz:\n```\n{conf_code}\n```", parse_mode="Markdown")
    msg = "🔑 Yangi kod olish uchun [/login](command) ni bosing"
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)

    cache.set(conf_code,
              {"phone_number": data['phone_number'], "username": data['username'], "password": data['password']}, 20)
    cache.set(message.from_user.id, str(conf_code), 20)

# @main_router.callback_query(F.data == "refresh"):
