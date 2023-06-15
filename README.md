# Проект JServiceQuestions — Сервис сбора уникальных вопросов с сайта https://jservice.io.
Сервис парсит информацию по вопросам с сайта https://jservice.io и сохраняет их в БД.
## Подготовка окружения для разработки

### Предварительные требования:
1. **Poetry** \
Зависимости и пакеты управляются через **poetry**. Убедитесь, что **poetry** [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/cli/).
```
- Устанавливаем Poetry версия 1.4.0
    curl -sSL https://install.python-poetry.org | python - --version 1.4.0
- Добавляем Poetry в переменную среды PATH
    "$HOME/.local/bin" для Unix.
    "%APPDATA%\Python\Scripts" для Windows.
```
2. **Docker**
3. Файлы **requirements** \
Файлы редактировать вручную не нужно. Обновление происходит автоматически через pre-commit хуки.
4. **pre-commit хуки** \
[Документация](https://pre-commit.com)\
При каждом коммите выполняются хуки перечисленные в **.pre-commit-config.yaml**.
Если при коммите возникает ошибка, можно запустить хуки вручную:
    ```
    pre-commit run --all-files
    ```

### Запуск проекта:
1. Клонировать репозиторий и перейти в него в командной строке:
    ```
    git clone git@github.com:agatinet31/jservice_questions.git
    cd jservice_questions
    ```
2. Убедитесь что poetry установлен. Активируйте виртуальное окружение. Установите зависимости
    ```
    poetry shell
    poetry install
    ```
3. Сделайте миграции
    ```
    alembic upgrade head
    ```
4. Установите pre-commit хуки
    ```
    pre-commit install --all
    ```
5. Убедитесь, что при запуске используется правильное виртуальное окружение.
Посмотреть путь можно следующей командой:
    ```
    poetry env info --path
    ```
## Использование
Создать и заполнить файл .env:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=masterkey
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=js
PGADMIN_DEFAULT_EMAIL: str = "admin@local.host"
PGADMIN_DEFAULT_PASSWORD: str = ""
PGADMIN_LISTEN_PORT: str = "8080"
SECRET=^SUPER@SECRET#
CORS_ORIGINS=["http://localhost:8000"]
```
В корневом каталоге проекта создайте образы и разверните контейнеры Docker:
```
docker-compose up -d --build
```
### Эндроинты сервиса
```
POST /api/question/ - добавление уникальных вопросов с сайта https://jservice.io
query параметр запроса:
    {"questions_num": integer}, где questions_num - количество уникальных вопросов, которые надо получить (не более 100)

Пример ответа сервиса для questions_num=3:
{
  "id": 72431,
  "answer": "Juvenile Delinquent",
  "question": "A J.D., which stands for this type of youth, may come from a broken home -- or just be bored",
  "value": 300,
  "airdate": "2001-05-18T23:00:00",
  "created_at": "2022-12-30T22:09:27.154000",
  "updated_at": "2022-12-30T22:09:27.154000",
  "category_id": 6903
}
```
### Документация API
Страница с документацией сервиса будет доступна по адресу:
```
http://127.0.0.1/docs и http://127.0.0.1/redoc
```

## Автор
Андрей Лабутин
