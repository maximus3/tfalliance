import sys
from aiogram import Bot, Dispatcher, executor, types
import logging

logger = logging.getLogger(__name__)
if len(sys.argv) < 2:
    logger.error('No token in argv')
token = sys.argv[1]
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
