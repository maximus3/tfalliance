from enum import IntEnum


class StatusCode(IntEnum):
    OK = 0
    THEME_ALREADY_EXISTS = 1
    ERROR_IN_ADD_TO_DATABASE = 2
