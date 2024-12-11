""""План написания админ панели"
Цель: написать простейшие CRUD функции для взаимодействия с базой данных.
Задача "Продуктовая база":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя
пунктам задачи ниже.
Дополните ранее написанный код для Telegram-бота:
Создайте файл crud_functions.py и напишите там следующие функции:
initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи
SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
title(название продукта) - текст (не пустой)
description(описание) - текст
price(цена) - целое число (не пустой)
get_all_products, которая возвращает все записи из таблицы Products, полученные
при помощи SQL запроса.
Изменения в Telegram-бот:
В самом начале запускайте ранее написанную функцию get_all_products.
Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной
нумерации продуктов функцию get_all_products. Полученные записи используйте в выводимой
надписи: "Название: <title> | Описание: <description> | Цена: <price>"
Перед запуском бота пополните вашу таблицу Products 4 или более записями для
последующего вывода в чате Telegram-бота.
"""

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import get_all_products

api = "7611654870:AAGpdYjItvQmqZCjVq5ynJeqXoIAKfRccAA"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.row(button_1, button_2)
button_3 = KeyboardButton(text='Купить')
kb.add(button_3)

kb_in_1 = InlineKeyboardMarkup()
kb_in_2 = InlineKeyboardMarkup()
in_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_button_3 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
in_button_4 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
in_button_5 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
in_button_6 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_in_1.add(in_button_1)
kb_in_1.add(in_button_2)
kb_in_2.add(in_button_3)
kb_in_2.add(in_button_4)
kb_in_2.add(in_button_5)
kb_in_2.add(in_button_6)

@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)

async def get_buying_list(message):
    images = ['image_1.png', 'image_2.png', 'image_3.png', 'image_4.png']
    products = [
        'Название: Product 1 | Описание: описание 1 | Цена: 100',
        'Название: Product 2 | Описание: описание 2 | Цена: 200',
        'Название: Product 3 | Описание: описание 3 | Цена: 300',
        'Название: Product 4 | Описание: описание 4 | Цена: 400'
    ]
    for i in get_all_products():
        number = i[0]
        title = i[1]
        description = i[2]
        price = i[3]
        with open (f'{str(number) + ".png"}', 'rb') as img:
                await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}')

    await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb_in_2)

    # for i in get_all_products():
    #     with open(images[i], 'rb') as img:
    #         await message.answer_photo(img, caption=products[i])
    # await message.answer('Выберите продукт для покупки:', reply_markup=kb_in_2)
class UserState (StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in_1)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора: 10 * вес + 6.25 * рост - 5 * возраст - 161')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age'])
    await message.answer(f"Необходимое количество каллорий: {calories}")
    await state.finish()

@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer("Введите команду /start, чтобы начать общение.")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


