# Mailing Service - Сервис рассылок (курсовой проект по Django)
## О проекте:
Сервис рассылок - позволяет создавать и управлять рассылками писем по заданным критериям для выбранных адресатов.
В данном сервисе реализованн следующий функционал:

- Создание адресатов рассылки
- Создание писем для рассылки
- Настройка времени и периодичности рассылки
- Возможность создания отложенной рассылки
- Логирование всех прошедших рассылок

## Настройка сервиса:
- Установлены Python версии не ниже 3.10, база данных PostgreSQL
- В директории проекта создано виртуальное окружение:
  
`python -m venv env`

- Установлены зависимости:
  
`pip install -r requirements.txt`

-Создана пустая БД в PostgreSQL
- Заполнен файл `.env.sample` вашими настройками и после переименован в `.env`
- Созданы и применены миграции:

`python manage.py makemigrations`
`python manage.py migrate`

- Запущен локальный сервер:
  
`python manage.py runserver`

## Дополнительные настройки:
- Суперпользователь создается командой:
  
`python manage.py csu` 

и имеет следующие настройки:

логин: admin@admin.ru

пароль: 123123123

## Начало работы:
Для начала работы пользователю необходимо создать либо авторизоваться под существующим аккаунтом в сервисе

Если пользователь проходит процедуру регистрации, после заполнения формы на электронную почту пользователя поступит письмо со ссылкой для активации аккаунта

После активации ссылки пользователь сможет:

Создавать клиентов для рассылки

Создавать письма для рассылки

Создавать рассылку с выбранными параметрами

# Логика работы системы:

После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания, то должны быть выбраны из справочника все клиенты, которые указаны в настройках рассылки, и запущена отправка для всех этих клиентов.

Если создается рассылка со временем старта в будущем, то отправка должна стартовать автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.

По ходу отправки сообщений должна собираться статистика по каждому сообщению для последующего формирования отчетов.

## Главная страница

На главной странице отображена информация:

количество рассылок всего,

количество активных рассылок,

количество уникальных клиентов для рассылок,

3 случайные статьи из блога.

## В сущности блога следующие поля:

заголовок,

содержимое статьи,

изображение,

количество просмотров,

дата публикации.
