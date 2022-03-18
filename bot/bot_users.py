import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
import asyncio
from os import getenv

TOKEN = getenv("BOT_TOKEN")  # берем токен из виртуального окружения
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    check = await check_admin_permissions(message.from_user.id)
    full_name = []
    for i in [message.from_user.first_name, message.from_user.last_name, message.from_user.username]:
        if i is not None:
            full_name.append(i)
    await message.answer(f"Здравствуйте, {full_name[0]}!\nВас приветствует бот компании МемасАльянс!")
    print(message.from_user)
    if check:
        await message.answer(f"{full_name[0]}, у Вас права модератора! Вы можете отвечать на сообщения пользователей.")
    else:
        await message.answer(f"{full_name[0]}, Вы можете отправлять сообщения модераторам для получения ответа на "
                             f"интересующий вопрос.")


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


@dp.message_handler(commands="incoming")
async def incoming(message: types.Message):
    check = await check_admin_permissions(message.from_user.id)
    if check:
        await message.answer("ПОКА ВОПРОСЫ НЕ НАПИСАНЫ")
    else:
        await message.answer("Данная команда не доступна для данного пользователя!")


# TODO Проверка того, что юзер администратор или нет
async def check_admin_permissions(user_id: int) -> bool:
    """
    :param user_id: уникальный идентификатор юзера
    :return: булевое значение являетлся ли юзер админом
    """

    return True


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
