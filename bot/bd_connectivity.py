from database.views import user_is_admin, get_messages

# TODO Проверка того, что юзер администратор или нет
def check_admin_permissions(user_id: int) -> bool:
    """
    :param user_id: уникальный идентификатор юзера
    :return: булевое значение являетлся ли юзер админом
    """

    return True


# TODO Доставать вопрос по ДАННОЙ ТЕМЕ бота из БД
def get_question(me) -> list:
    """

    :return: должен выдавать список вопросов ['','', ...] если их нет то []
    """
    print(me)
    question = []
    question = ["What are u", "Сообщение номер 2", "Сообщение номер 3"]  # Если в БД есть запись с данной ТЕМОЙ и
    # completed == false -> вставляем текст сообщения
    return question


