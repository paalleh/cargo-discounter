# Грузовой дискаунтер 

## Описание проекта 
Предлагаемый сервис поможет свести напрямую Водителя и Заказчика через телеграмм-бота. Водитель регистрируется и получает уведомления о заказах в интересующем его районе. Заказчик указывает маршрут, выбирает нужные опции (грузчик, экспедитор итд) и предлагает цену. Для удобства Заказчик сможет скинуть в бота скриншот заказа из Яндекс.Го. Ответы на заявки с предложениями водителей будет отправлены для рассмотрения заказчика, где он сможет выбрать наиболее выгодное для себя предложение. После акцентирования заявки Заказчик получает номер телефона водителя.

## Python version
> Python 3.12

## Как комитить и мержить в проект
> Изменеия в мастер вносятся строго через PullRequest
- Все изменения ведуться в отдельных ветках (название ветки `<tiket_num>_<tiket_name>` Пример: `12_create_auth_page`)

- ### Соглашение о коммитах
```
<тип>(<область>): <краткое описание>

[Тело коммита]

[Футер коммита]
```
- <тип>: Обозначает тип изменений, например:

- - feat: Добавление новой функциональности
- - fix: Исправление ошибок
- - docs: Изменения в документации
- - refactor: Рефакторинг существующего кода без изменения его функциональности
- - test: Добавление или исправление тестов


- <область> (необязательно): Обозначает область или компонент, к которому относятся изменения (например, frontend, backend, tests).


- <краткое описание>: Краткое и понятное описание изменений.


- #### Пример:
- - ```feat(tg_bot_customer): Добавить кнопку "Войти"```
- - ```fix(backend): Исправить ошибку при сохранении данных пользователя```
- - ```docs: Обновление README``` (Изменения дневника разработки тоже docs)
- - ```refactor(backend): Оптимизировать запрос к базе данных```
- - ```test: Добавить юнит-тесты для сервиса аутентификации```


- [Тело коммита] (необязательно): Дополнительная информация о внесенных изменениях, их целях и важности.


- [Футер коммита] (обязательно): Номера тикета + название тикета


- #### Пример:

```
feat(frontend): Добавить кнопку "Войти"

Добавлена новая кнопка для аутентификации пользователей.

Связанные тикеты: #12 Создание страницы аутентификации
```

## Как собрать проект локально

### Локальная сборка

- Склонировать репозитроий на свой компьютер
- Установить все зависомсти из requirements.txt
- Создать файл .env по шаблону из .env.tmpl (файл необходимо создать рядом с .env.tmpl)
- Прокинуть миграции к вашей базе данных с помощью команды `alembic upgrade head`
- Для запуска backend прилжения необходимо запустить файл backend/main.py
- > Swagger: http://localhost:9000/docs

### Запуск через Docker

- Склонировать репозитроий на свой компьютер
- Создать файл .env по шаблону из .env.tmpl (файл необходимо создать рядом с .env.tmpl)
- Запустить docker-compose.dev.yml
- > Swagger: http://localhost:9000/docs

> Полезные команды для работы с docker и docker-compose
- Собрать: `docker-compose -f docker-compose.dev.yml build`
- Запустить: `docker-compose -f docker-compose.dev.yml up -d`
- Убить: `docker-compose -f docker-compose.dev.yml down -v`
- Посмотреть список всех активных контейнеров: `docker ps`
- Посмотреть список всех контейнеров: `docker ps -a`
- Посмотреть логи контейнера: `docker logs -f <container id/container name>`

#### Работа с alembic в docker

Чтобы работать с командами alembic, например прокинуть миграции необходимо:

- Зайти внутрь необходимого контейнера: `docker-compose -f docker-compose.dev.yml exec <имя контейнера> bash` 
- Выполнить необходимую команду: `alembic upgrade head`

## Работа с alembic
- После изменений в структуре бд необходимо выполнить команду: `alembic revision --autogenerate -m "Комментарий к изменениям"`
- Применить изменения: `alembic upgrade head`