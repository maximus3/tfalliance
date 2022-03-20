from aiogram.dispatcher.filters.state import State, StatesGroup


class Butts:
    moderator_main_menu = [
        ['Ответить на вопрос'],
        ['Предыдущий', 'Текущий', 'Следующий'],
        ['Получить список вопросов'],
    ]
    cancel_menu = [['Отмена']]


class Answer(StatesGroup):
    question_answer = (
        State()
    )  # Will be represented in storage as 'Answer:question_answer'


class CurrentMessage:
    def __init__(self):
        self.current_index_of_message = 0

    def current_i(self):
        return self.current_index_of_message

    def next_i(self):
        self.current_index_of_message += 1

    def prev_i(self):
        self.current_index_of_message -= 1

    def reset_i(self):
        self.current_index_of_message = 0
