import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from os import getenv

TOKEN = getenv("BOT_TOKEN")  # берем токен из виртуального окружения
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    question_answer = State()  # Will be represented in storage as 'Form:name'


@dp.message_handler(commands="incoming")
@dp.message_handler(Text(equals='Ответить', ignore_case=True))
async def incoming(message: types.Message):
    check = await check_admin_permissions(message.from_user.id)
    if check:
        question = await get_question()
        if question == "":
            pass
        else:
            await Form.question_answer.set()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Отмена"]
            keyboard.add(*buttons)
            await message.answer(question, reply_markup=keyboard)
    else:
        await message.answer("Данная команда не доступна для данного пользователя!")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And add main menu keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    check = await check_admin_permissions(message.from_user.id)
    if check:
        buttons = ["Отправить", "Помощь"]
        keyboard.add(*buttons)
        await message.answer('Главное меню модератора', reply_markup=keyboard)
    else:
        #  TODO В случае обычного пользователя прописать.....
        pass


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    check = await check_admin_permissions(message.from_user.id)
    full_name = []
    for i in [message.from_user.first_name, message.from_user.last_name, message.from_user.username]:
        if i is not None:
            full_name.append(i)
    await message.answer(f"Здравствуйте, {full_name[0]}!\nВас приветствует бот компании МемасАльянс!")
    print(message.from_user)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if check:
        buttons = ["Отправить", "Помощь"]
        keyboard.add(*buttons)
        await message.answer('Главное меню модератора', reply_markup=keyboard)
    else:
        #  TODO В случае обычного пользователя прописать.....
        pass


@dp.message_handler(Text(equals="Помощь"))
@dp.message_handler(commands="help")
async def helping(message: types.Message):
    check = await check_admin_permissions(message.from_user.id)
    if check:
        await message.answer("Список доступных команд для Модератора:\n"
                             "/start - инициализация, старт работы бота\n"
                             "/help - вывод данного меню\n"
                             "/incoming - начать отвечать на вопрос")
    else:
        await message.answer("Список доступных команд для пользователя:\n"
                             "/start - инициализация, старт работы бота\n"
                             "/help - вывод данного меню\n"
                             "/write - написать сообщение модератору")


# TODO Проверка того, что юзер администратор или нет
async def check_admin_permissions(user_id: int) -> bool:
    """
    :param user_id: уникальный идентификатор юзера
    :return: булевое значение являетлся ли юзер админом
    """

    return True


# TODO Доставать вопрос по ДАННОЙ ТЕМЕ бота из БД
async def get_question():
    question = ""
    question = "What are u"  # Если в БД есть запись с данной ТЕМОЙ и completed == false вставляем текст сообщения
    return question


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
