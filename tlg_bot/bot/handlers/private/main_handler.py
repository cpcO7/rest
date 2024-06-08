from random import randint

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
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
            user = await sync_to_async(User.objects.get)(username=message.text)
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

    await message.answer(f"🔒 Kodingiz: {conf_code}")

    cache.set(conf_code,
              {"phone_number": data['phone_number'], "username": data['username'], "password": data['password']}, 300)
