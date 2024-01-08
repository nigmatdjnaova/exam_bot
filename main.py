import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot_token = ("6426612496:AAHbTvmT3tuxO1FXG6zcbMx0Lb-EPlbOj74")

storage = MemoryStorage()

pattern = re.compile(r'^\+998[0-9]{9}')
pattern1 = re.compile(r'^[0-9]')

class Partner(StatesGroup):
    full_name = State()
    phone_number = State()
    age = State()
    email = State()


bot = Bot(str(bot_token))
dp = Dispatcher(bot, storage=storage)
async def on_startup(_):
    print("Bot ishga tushdi") 



def start_buttons() -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="Kanalga havola")
    button2 = KeyboardButton(text="Tekshirish")  
    button3 = KeyboardButton(text="Ro'yhatdan o'tish")
    buttons.add(button1, button2)
    buttons.add(button3)
    
    return buttons    


@dp.message_handler(commands=['start'])
async def start_button(message: types.Message):
    first_name = message.from_user.first_name
    text = f"Assalomu alaykum {first_name} \nbotga xush kelibsiz!\nBotdan foydalanish uchun kanalga obuna bo'ling!"
    await message.answer(text=text, reply_markup=start_buttons())




@dp.message_handler(Text(equals="Kanalga havola"), state="*")
async def btn2(message: types.Message):
    text= "Kanal havolasi:\n https://t.me/+txhH2BCiQ-EwYzBi"
    await Partner.full_name.set()
    await Partner.next() 


@dp.message_handler(Text(equals="Tekshirish"), state="*")
async def btn2(message: types.Message):
    text= "Kanalga a'zo bo'lganligingiz tekshirilmoqda"
    await Partner.full_name.set()

@dp.callback_query_handler(text='look_sub')
async def lcallback_query_keyboard(callback_query: types.CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id='_', user_id = callback_query.from_user.id)
    if user_channel_status["status"] != 'left':
        await bot.send_message(
            callback_query.from_user.id,
            'ok'
        )
    else:
        await bot.send_message(callback_query.from_user.id, 'not ok,subscribe please, reply_mark_up=keyboard_chat') 

@dp.message_handler(Text(equals="Ro'yhatdan o'tish"), state="*")
async def btn2(message: types.Message):
    text= "Ro'yhatdan o'tish boshlandi. Hozir sizga bir necha savollar beriladi.\n To'liq ismingizni kiriting"
    await Partner.full_name.set()


@dp.message_handler(state=Partner.full_name)
async def set_full_name(message: types.Message, state: FSMContext):
    text = "Telefon raqamingizni kiriting"
    await state.update_data(full_name=message.text)

    await message.answer(text=text)

    await Partner.next() 


@dp.message_handler(state=Partner.phone_number)
async def set_phone_number(message: types.Message, state: FSMContext):
    if pattern.match(message.text):
       text = "🕑 Yosh: \n\nYoshingizni kiriting?\nMasalan, 19" 
       await state.update_data(phone_number=message.text)

       await message.answer(text=text)

       await Partner.next()    
  
    else:
        await message.answer("Togri telefon raqam kirgizing")



@dp.message_handler(state=Partner.age)
async def set_age(message: types.Message, state: FSMContext):
    text = "E-mail ni kiriting" 
    await state.update_data(age=message.text)

    await message.answer(text=text)

    await Partner.next()    



    

@dp.message_handler(state=Partner.email)
async def set_email(message: types.Message, state: FSMContext):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="HA")
    button2 = KeyboardButton(text="YOQ")
    buttons.add(button1,button2)
    await state.update_data(email=message.text)

    data = await state.get_data()

    text = f"To'liq ism{data['full_name']}\nTelefon_raqami: {data['phone_number']}\nTelegram: @{message.from_user.username}\nYoshi: {data['age']}\nEmail: {data['email']}\n\nBarcha malumotlar to'g'rimi"

    await message.answer(text=text, reply_markup=buttons)

    await Partner.next()

@dp.message_handler(Text(equals="HA"))
async def set_application(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = f"To'liq ism{data['full_name']}\nTelefon_raqami: {data['phone_number']}\nTelegram: @{message.from_user.username}\nYoshi: {data['age']}\nEmail: {data['email']}\n\nBarcha malumotlar to'g'rimi"
    print(message.from_user.id)
    await bot.send_message(chat_id="6550264522", text=text)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  

