import logging

from config import BASE_DIR

logging.basicConfig(
    format='%(filename)s %(funcName)s [LINE:%(lineno)d]# %(levelname)-8s '
    '[%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO,
    filename=BASE_DIR / 'bot' / 'bot.log',
)
