DEFAULT_REQUEST_ERROR_MSG = "Ошибка получения данных c эндпоинта!"


class QuestionError(Exception):
    """Класс исключения по вопросам."""

    pass


class QuestionRequestError(QuestionError):
    """Класс исключения при запросе информации."""

    def __init__(
        self, jservice_url, questions_num, message=DEFAULT_REQUEST_ERROR_MSG
    ):
        self.jservice_url = jservice_url
        self.questions_num = questions_num
        super().__init__(
            f"{message} URL: {jservice_url}. "
            f"Количество запрашиваемых вопросов={questions_num}."
        )


class QuestionIncorrectStructureError(QuestionRequestError):
    """Класс исключения при неверной структуре данных."""

    def __init__(self, *args):
        super().__init__(
            *args, message="Получена неверная структура данных!"
        )


class QuestionLenError(QuestionRequestError):
    """
    Класс исключения при получение неверного
    количества данных с хостинге.
    """

    def __init__(self, *args):
        super().__init__(*args, message="Получены не все данные с хостинга!")


class QuestionDBNotFoundError(QuestionError):
    """Класс исключения при отсутствии информации в базе данных."""

    def __init__(self, question_id):
        self.project_id = question_id
        super().__init__(
            f"Вопрос с идентификтором {question_id} не найден в БД!"
        )
