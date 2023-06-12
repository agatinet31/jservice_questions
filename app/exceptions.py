DEFAULT_REQUEST_ERROR_MSG = 'Ошибка получения данных товара c эндпоинта!'


class ProductError(Exception):
    """Класс исключения по товарам."""
    pass


class QuestionRequestError(ProductError):
    """Класс исключения при запросе информации по товару."""
    def __init__(self, product_card_url, product_id, message=DEFAULT_REQUEST_ERROR_MSG):
        self.product_card_url = product_card_url
        self.product_id = product_id
        super().__init__(
            f'{message} URL: {product_card_url}. ID={product_id}.'
        )


class QuestionIncorrectStructureError(QuestionRequestError):
    """Класс исключения при неверной структуре данных товара."""
    def __init__(self, *args):
        super().__init__(
            *args,
            message='Получена неверная структура данных по товару!'
        )


class ProductHostingNotFoundOnError(QuestionRequestError):
    """Класс исключения при отсутствии информации по товару на хостинге."""
    def __init__(self, *args):
        super().__init__(
            *args,
            message='Товар не найден на хостинге!'
        )


class ProductDBNotFoundError(ProductError):
    """Класс исключения при отсутствии информации по товару в базе данных."""
    def __init__(self, product_id):
        self.project_id = product_id
        super().__init__(
            f'Товар с идентификтором {product_id} не найден в БД!'
        )


class UniqueProductNameError(ProductError):
    """Класс исключения уникальности имени продукта."""
    def __init__(self, product_name):
        self.project_name = product_name
        super().__init__(
            f'Товар с наименованием `{product_name}` уже существует!'
        )
