from enum import Enum


class StatusCode(Enum):
    OK = 0
    THEME_ALREADY_EXISTS = 1
    ERROR_IN_ADD_TO_DATABASE = 2