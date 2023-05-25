# Задача 1

Сервис позволяет получать необходимое количество вопросов для викторины с jservice.io и сохранять их в базе данных

## Скачивание проекта и подготовка файлов:

### Создайте папку:
```bash
mkdir task_1
```

### Перейдите в папку:
```bash
cd task_1
```
### Скачайте репозиторий:
```bash
git clone ******************** 
```

### Перейдите в папку проекта:
```bash
cd questions
```

### Создйте .env файл:
```bash
touch .env
```

### В .env файле укажите данные своей базы данных.
Пример наполнения можно увидеть в файле .env_example:
```bash
POSTGRES_DB=questions_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Создание и запуск контейнера:

### Сборка образов и запуск котейнеров:

```bash
docker-compose up -d --build
```
### Остановка контейнеров:
```bash
docker-compose stop
```
### Повторный запуск контейнеров:
```bash
docker-compose up
```
Данные БД хранятся в volumes

## Инициализация БД (выполняется внутри контейнера):
```bash
docker-compose exec app bash
```
```bash
flask db init
flask db migrate
flask db upgrade
```

## Пример запроса:
```bash
curl --header "Content-Type: application/json" --request POST --data '{"questions_num":7}'  http://localhost:5000
```
Цифра после "questions_num" - количество вопросов, которые вы хотите получить.

## Пример ответа (для "questions_num":1):
```
{"question_id":198810,"question":"Gods suspended above the stage in ancient drama gave rise to this Latin phrase for something that saves the day","answer":"<i>deus ex machina</i>","date":"Fri, 30 Dec 2022 21:43:28 GMT"}
```
### Как подключиться к БД:
```bash
docker-compose exec db psql questions_db -U postgres
```
### Примеры запросов к БД:
```bash
SELECT * FROM questions_db;

SELECT question FROM questions_db;
```

## Автор:
Анатолий Коновалов (BobHawler)