# Doomer Bot

Телеграм бот на питоне с использованием python-telegram-bot:

## Пользовательские команды

| Команда     | Описание                                                                   |
| ----------- | -------------------------------------------------------------------------- |
| start       | Инициальное сообщение бота                                                 |
| slap        | Кого-то унизить (надо ответить жертве, чтобы бот понял кого бить)          |
| duel        | Устроить дуэль (надо ответить тому, с кем будет дуэль)                     |
| duelscore   | Мой счёт в дуэлях                                                          |
| duelranking | Ранкинг дуэлей чата (показывает только тех, у кого есть убийства и смерти) |
| pidor       | Пидор дня (новый пидор каждый день по немецкому времени)                   |
| pidorme     | Сколько раз вы были пидором дня                                            |
| pidorstats  | Статы чата по пидорам дня                                                  |
| flip        | Бросить монетку (Орёл/Решка)                                               |
| dog         | Случайное фото собачки                                                     |
| cat         | Случайное фото котика                                                      |
| help        | Меню помощи                                                                |
| whatsnew    | Новое в боте                                                               |
| adminmenu   | Админское меню                                                             |

## Админ команды (Для групп)

| Команда    | Описание                                                          |
| ---------- | ----------------------------------------------------------------- |
| leave      | Сказать боту уйти                                                 |
| duelstatus | Включить/Выключить дуэли (on/off)                                 |
| immune     | Добавить пользователю иммунитет на задержку команд (ответить ему) |
| unimmune   | Снять иммунитет (ответить или имя)                                |
| immunelist | Лист людей с иммунитетом                                          |

## Команды разработчика

| Команда     | Описание           |
| ----------- | ------------------ |
| allcommands | Все команды бота   |
| getlogs     | Получить логи бота |
| getdatabase | Получить датабазу  |

## Необходимо

* Python 3.7.5 (тестировалось на этой версии)
* [python-telegram-bot](https://github.com/leandrotoledo/python-telegram-bot) модуль (тестировалось с версией 12.4.1)

## Как использовать

* Клонировать репозиторию
* Добавить или сменить переменную среды "TG_BOT_TOKEN" (токен бота) на вашу
* Сменить DEVS в constants.py на свой айди пользователя в телеграме
* Запустить
