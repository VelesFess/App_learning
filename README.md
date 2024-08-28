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
````
 события ()
 добавитьь функцию списка событий по пользователю /events/ @get       user_id из токена # noqa: E501
 добавления события /events/   @post
 удаления события /events/{id_event} @ delete
 получения события /events/{id_event} @get
 получения события на дату /events/?date={event_date} @get
 дата пользователь(форм кей ) id (праймари) название(ограничить по длине ) коментарий # noqa: E501

 event_date format = YYYY-mm-dd
````