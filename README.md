## My project for learning new skills

This app will be used as calendar
Users will be authorised through the system to manage shedule
Shedule will be represented as Postgress DataBase.


## Накат миграций
```
alembic upgrade head
```

## Создание новой миграции
```
alembic revision --autogenerate -m "COMMENT"
```

## Todo tasks

  ~~события ()~~
 ~~добавитьь функцию списка событий по пользователю /events/ @get       user_id из токена # noqa: E501~~
~~добавления события /events/   @post~~
 ~~удаления события /events/{id_event} @ delete~~
 ~~получения события /events/{id_event} @get~~
 ~~получения события на дату /events/?date={event_date} @get~~
 ~~дата пользователь(форм кей ) id (праймари) название(ограничить по длине ) коментарий # noqa: E501~~

 Покрыть ручки интеграционными тестами. Интеграционные тесты - это когда ты дергаешь ручку и проверяешь корректность ее работы

 Что нужно проверить:
 1) Авторизация (валидный кейс, неверные данные, неверная структура данных)
 2) Пользователи (все ручки)
 3) События (все ручки)

Уделить внимание входным данным, проверять невалидные кейсы (не полностью заполненные данные, неверные форматы данных, большие данные и прочее)
