import logging
import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from config import token, admin
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

Tasdiqlash = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Tasdiqlash ✅"), KeyboardButton(text="Bekor qilish ❌")]
    ], resize_keyboard=True
)


class FormUser(StatesGroup):
    ism = State()
    bots = State()
    til = State()
    finish = State()


dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)




@dp.message(CommandStart())
async def StartBot(message: Message, state: FSMContext):
    await message.answer("Assalomu alaykum ismingizni kiriting?")
    await state.set_state(FormUser.ism)

@dp.message(F.text, FormUser.ism)
async def IsmBot(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(first=name)
    await message.answer("Bot yasashga qiziqasizmi?")
    await state.set_state(FormUser.bots)

@dp.message(F.text, FormUser.bots)
async def BotYasashBot(message: Message, state: FSMContext):
    xabar = message.text
    if xabar.lower() == "ha":
        await message.answer("Qaysi tildan foydalangan holda bot yozasiz")
        await state.update_data({"ha":xabar})
        await state.set_state(FormUser.til)
    elif xabar.lower() == 'yoq':
        await message.answer("Siz bilan o'zimiz bog'lanamiz?")
        await state.clear()
    else:
        await message.answer("Bot yasashga qiziqasizmi?")
        await state.set_state(FormUser.bots)        

@dp.message(F.text, FormUser.til)
async def TIlBOt(message: Message, state: FSMContext):
    dasturlash = message.text
    await state.update_data(dasturlash=dasturlash)
    data = await state.get_data()
    ismi = data.get("first")
    qiziqish = data.get("ha")
    await message.answer(f"Ism: {ismi}\nBotga qiziqish: {qiziqish}\nDasturlash tili: {dasturlash}\nMalumotlaringizni tasdiqlaysizmi?", reply_markup=Tasdiqlash)
    await state.set_state(FormUser.finish)

@dp.message(F.text, FormUser.finish)
async def FinishBot(message: Message, state: FSMContext):
    xabar = message.text
    data = await state.get_data()
    ismi = data.get("first")
    qiziqish = data.get("ha")
    dasturlash = data.get("dasturlash")
    if xabar == "Tasdiqlash ✅":
        await bot.send_message(chat_id=admin, text=f"Ism: {ismi}\nBotga qiziqish: {qiziqish}\nDasturlash tili: {dasturlash}")
        await bot.send_message(chat_id=-1002433028099, text=f"Ism: {ismi}\nBotga qiziqish: {qiziqish}\nDasturlash tili: {dasturlash}")
        await message.answer("Malumotlaringiz yuborildi")
        await state.clear()
    else:
        await message.answer("ismingizni qayta kiriting ?")
        await state.set_state(FormUser.ism)


async def main():
    await bot.send_message(chat_id=admin, text="Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print("tugadi")
