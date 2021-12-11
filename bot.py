from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ChatType
from aiogram.utils.callback_data import CallbackData
import logging
import quote
import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Callback_all
c = CallbackData('vote', 'action')
first_quote = InlineKeyboardButton('Другая цитата #1', callback_data=c.new('first_change_quote'))
second_quote = InlineKeyboardButton('Другая цитата #2', callback_data=c.new('second_change_quote'))
keys = [first_quote, second_quote]
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_generate = KeyboardButton('Цитата')
keyboard.add(button_generate)


# Handlers


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    quote_msg = quote.quote_better()
    await message.answer('Привет. Вот первая цитата, остальные можно получить по нажатию кнопок под сообщением.'
                         '\nКнопка "Друая цитата" выбирает новую цитату в этом же сообщении.'
                         '\nКнопка "Цитата" создает новое сообщение с кнопками реролла.',
                         reply_markup=keyboard)
    inline_kb = InlineKeyboardMarkup().add(*keys)
    await message.answer(quote_msg, reply_markup=inline_kb)


@dp.message_handler(lambda message: message.text == 'Цитата')
async def message_qoute(message: types.Message):
    quote_msg = quote.quote_generator()
    inline_kb = InlineKeyboardMarkup().add(*keys)
    await message.answer(quote_msg, reply_markup=inline_kb)


@dp.callback_query_handler(c.filter(action=['first_change_quote']))
async def callback_change_message(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id, text='Цитата изменена по вариату #1'
                                    , show_alert=False)
    quote_msg = quote.quote_better()
    if quote_msg == callback_query.message.text:
        quote_msg = quote.quote_better()
    inline_kb = InlineKeyboardMarkup().add(*keys)
    await bot.edit_message_text(text=quote_msg, chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id, reply_markup=inline_kb)


@dp.callback_query_handler(c.filter(action=['second_change_quote']))
async def callback_change_message(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id, text='Цитата изменена по вариату #2'
                                    , show_alert=False)
    quote_msg = quote.quote_generator()
    if quote_msg == callback_query.message.text:
        quote_msg = quote.quote_generator()

    inline_kb = InlineKeyboardMarkup().add(*keys)
    await bot.edit_message_text(text=quote_msg, chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id, reply_markup=inline_kb)


# StartBot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
