from enum import IntEnum


class StatusCode(IntEnum):
    OK = 0
    WRONG_PARAMETERS_COUNT = 1
    ERROR_IN_ADD_TO_DATABASE = 2
    ERROR_IN_REGISTER_NEW_BOT = 3
    RUN_BOT_ERROR = 4
    ERROR_THEME_ALREADY_EXISTS = 5
    ERROR_WRONG_CODE = 6
