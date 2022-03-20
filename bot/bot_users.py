import logging
from bd_connectivity import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from os import getenv
from But import *

TOKEN = getenv("BOT_TOKEN")  # берем токен из виртуального окружения
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
QUESTIONS = []
current_class = CurrentMessage()  # Экзепляр класса с текущим значением message index


#  TODO Добавить класс Request для обычных юзеров


async def update_list_of_questions():
    global QUESTIONS
    me = await bot.get_me()
    QUESTIONS = get_question(me)  # Вызов функции для возврата массива вопросов ["213","sadasd", ....]


#  (Доступно только для админа) Выдает текст вопроса от пользователя и стартует STATE question answer
@dp.message_handler(commands="incoming")
@dp.message_handler(Text(equals='Ответить на вопрос', ignore_case=True))
async def incoming(message: types.Message):
    check = check_admin_permissions(message.from_user.id)
    if check:
        print(current_class.current_i() + 1)
        if not QUESTIONS:
            await message.answer("Сообщений по данной теме пока нет!")
        else:
            if 0 <= current_class.current_i() < len(QUESTIONS):
                question_current = QUESTIONS[current_class.current_i()]
                await Answer.question_answer.set()  # start STATE
                text = f"Вопрос номер - {current_class.current_i() + 1}\n\n" \
                       f"{question_current}"
                await message.answer(text, reply_markup=add_buttons_to_keyboard(Butts.cancel_menu))
            else:
                print(f"Ошибка!\nДанного сообщения не существует")
                await message.answer("Ошибка!\nДанного сообщения не существует!")
    else:
        await message.answer("Данная команда не доступна для данного пользователя!")


@dp.message_handler(Text(equals='Получить список вопросов', ignore_case=True))
async def get_list_of_messages(message: types.Message):
    await update_list_of_questions()
    await message.answer("Получаю список вопросов...")
    if not QUESTIONS:
        await message.answer("Пока нет новых сообщений по данной теме")
    else:
        await message.answer(f"У Вас есть неотвеченные вопросы: {len(QUESTIONS)}")
        await message.answer(f"Вопрос номер - {current_class.current_i() + 1}\n\n"
                             f"{QUESTIONS[current_class.current_i()]}")


@dp.message_handler(Text(equals='Следующий', ignore_case=True))
async def next_question(message: types.Message):
    if not QUESTIONS:
        await message.answer("Пока нет новых сообщений по данной теме")
    else:
        if 0 <= current_class.current_i() + 1 < len(QUESTIONS):
            current_class.next_i()
            await message.answer(f"Вопрос номер - {current_class.current_i() + 1}\n\n"
                                 f"{QUESTIONS[current_class.current_i()]}")
        else:
            await message.answer(f"Нет вопроса...")


@dp.message_handler(Text(equals='Предыдущий', ignore_case=True))
async def next_question(message: types.Message):
    if not QUESTIONS:
        await message.answer("Пока нет новых сообщений по данной теме")
    else:
        if 0 <= current_class.current_i() - 1 < len(QUESTIONS):
            current_class.prev_i()
            await message.answer(f"Вопрос номер - {current_class.current_i() + 1}\n\n"
                                 f"{QUESTIONS[current_class.current_i()]}")
        else:
            await message.answer(f"Нет вопроса...")


@dp.message_handler(Text(equals='Текущий', ignore_case=True))
async def next_question(message: types.Message):
    if not QUESTIONS:
        await message.answer("Пока нет новых сообщений по данной теме")
    else:
        if 0 <= current_class.current_i() < len(QUESTIONS):
            await message.answer(f"Вопрос номер - {current_class.current_i() + 1}\n\n"
                                 f"{QUESTIONS[current_class.current_i()]}")
        else:
            await message.answer(f"Нет вопроса...")


#  ОТМЕНА действия и возврат в главное меню при любом STATE для любого пользователя
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
    check = check_admin_permissions(message.from_user.id)
    if check:
        await message.answer('Главное меню модератора', reply_markup=add_buttons_to_keyboard(Butts.moderator_main_menu))
    else:
        pass


# await message.answer('Главное меню пользователя', reply_markup=) #  TODO Добавить кнопки для обычного пользователя!


# STATE для Answer - вызывается при вводе текста после написанного вопроса
@dp.message_handler(state=Answer.question_answer)
async def process_question_answer(message: types.Message, state: FSMContext):
    print(message.text)  # TODO отправить данный текст для пользователя написавшего запрос
    await message.forward(chat_id=154616634)
    await message.answer("Success!", reply_markup=add_buttons_to_keyboard(Butts.moderator_main_menu))
    await state.finish()


#  Обработка исключения, когда пользователь заблокировал бота
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


def add_buttons_to_keyboard(buttons):
    """
    Функция добавляет определенные кнопки
    :param buttons: Подается двумерный массив кнопок для вывода пользователю
    :return: получившийся keyboard
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        keyboard.add(*button)
    return keyboard


# СТАРТ, ИНИЦИАЛИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ И БОТА
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    check = check_admin_permissions(message.from_user.id)
    full_name = []
    for i in [message.from_user.first_name, message.from_user.last_name, message.from_user.username]:
        if i is not None:
            full_name.append(i)
    await message.answer(f"Здравствуйте, {full_name[0]}!\nВас приветствует бот компании МемасАльянс!")
    print(message.from_user)
    if check:
        await message.answer('Главное меню модератора', reply_markup=add_buttons_to_keyboard(Butts.moderator_main_menu))
    else:
        pass
        # await message.answer('Главное меню пользователя', reply_markup=keyboard) # TODO Добавить кнопки для
        #  обычного пользователя!


# Вывод меню помощи для каждого пользователя
@dp.message_handler(Text(equals="Помощь"))
@dp.message_handler(commands="help")
async def helping(message: types.Message):
    check = check_admin_permissions(message.from_user.id)
    if check:
        await message.answer("Для модератора доступны кнопки ниже\n\n"
                             "Для получения спсика вопросов нажмите 'Получить список вопросов'\n\n"
                             "После получения списка, вы можете приступать к написанию ответов\n\n"
                             "Вопросы можно пролистывать с помощью кнопок переключения\n\n"
                             "Если Вы нажали на кнопку 'Ответить на вопрос', то к данному вопросу можно писать "
                             "ответ\n\n "
                             "Если Вы не хотите отвечать на данный вопрос, нажмите появившуюся кнопку 'Отмена'\n\n")
    else:
        await message.answer("ПОКА ПУСТО")  # TODO написать Помощь для user


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
