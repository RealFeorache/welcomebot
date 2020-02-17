"""Telegram bot based on python-telegram-bot with various commands."""

from telegram.ext import (CommandHandler, Filters,
                          MessageHandler)
from datetime import time

import main.commands as commands
from main import LOGGER, dispatcher, textfiltering, updater
from main.helpers import error_callback, ping, db_backup


# Bot commands
USERCOMMANDS = [
    'Команды для рядовых пользователей',
    ('slap', commands.slap,
     'Кого-то унизить (надо ответить жертве, чтобы бот понял кого бить)'),
    ('duel', commands.duel,
     'Устроить дуэль (надо ответить тому, с кем будет дуэль)'),
    ('duelscore', commands.duelscore, 'Мой счёт в дуэлях'),
    ('duelranking', commands.duelranking,
     'Ранкинг дуэлей чата (показывает только тех, у кого есть убийства и смерти)'),
    ('pidor', commands.pidor,
     'Пидор дня (новый пидор каждый день по немецкому времени)'),
    ('pidorme', commands.pidorme, 'Сколько раз вы были пидором дня'),
    ('pidorstats', commands.pidorstats, 'Статы чата по пидорам дня'),
    ("flip", commands.flip, 'Бросить монетку (Орёл/Решка)'),
    ("dadjoke", commands.dadjoke, 'Случайная шутка бати'),
    ("dog", commands.animal, 'Случайное фото собачки'),
    ("cat", commands.animal, 'Случайное фото котика'),
    ("help", commands.bothelp, 'Меню помощи'),
    ('whatsnew', commands.whatsnew, 'Новое в боте'),
    ('adminmenu', commands.adminmenu, 'Админское меню'),
]
ONLYADMINCOMMANDS = [
    'Команды для администраторов групп',
    ('setcooldown', commands.setcooldown, 'Поставить новую задержку на команды'),
    ('duelstatus', commands.duelstatus, 'Включить/Выключить дуэли (on/off)'),
    ('immune', commands.immune,
     'Добавить пользователю иммунитет на задержку команд (ответить ему)'),
    ('unimmune', commands.unimmune, 'Снять иммунитет (ответить или имя)'),
    ('immunelist', commands.immunelist, 'Лист людей с иммунитетом'),
    ('leave', commands.leave, 'Сказать боту уйти')
]
UNUSUALCOMMANDS = [
    'Нечастые команды',
    ('allcommands', commands.allcommands, 'Все команды бота'),
    ('start', commands.start, 'Начальное сообщение бота'),
    ('getlogs', commands.getlogs,
     'Получить логи бота (только для разработчика)'),
    ('getdatabase', commands.getdatabase, 'Получить датабазу'),
    ('promote', commands.promote, 'Хехехехе')
]


def main():
    """Main function."""
    LOGGER.info('Adding handlers...')
    # Add command handles
    for commandlists in (USERCOMMANDS, ONLYADMINCOMMANDS, UNUSUALCOMMANDS):
        for command in commandlists[1:]:
            dispatcher.add_handler(CommandHandler(
                command[0], command[1],
                filters=(~Filters.update.edited_message & Filters.command)))
    # Add message handlers
    dispatcher.add_handler(MessageHandler(
        (Filters.status_update.new_chat_members &
         ~Filters.update.edited_message), textfiltering.welcomer))
    dispatcher.add_handler(MessageHandler(
        (Filters.status_update.left_chat_member &
         ~Filters.update.edited_message), textfiltering.farewell))
    dispatcher.add_handler(MessageHandler(
        (Filters.text &
         ~Filters.update.edited_message), textfiltering.message_filter))
    # Log errors
    dispatcher.add_error_handler(error_callback)
    # Add job queue
    updater.job_queue.run_repeating(
        callback=ping, interval=60 * 60, first=0)
    updater.job_queue.run_daily(
        callback=db_backup, time=time(0, 0, 0, 0))
    # Start polling
    updater.start_polling(clean=True)
    LOGGER.info('Polling started.')
    LOGGER.info('-----------------------------------------------')
    updater.idle()


if __name__ == '__main__':
    main()
