from enum import IntEnum


class StatusCode(IntEnum):
    OK = 0
    THEME_ALREADY_EXISTS = 1
    ERROR_IN_ADD_TO_DATABASE = 2
    THEME_NOT_EXISTS = 3
    CHAT_NOT_EXISTS = 4
    CHAT_ALREADY_EXISTS = 5
