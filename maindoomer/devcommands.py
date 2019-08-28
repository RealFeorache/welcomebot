"""
Module dedicated to commands available only to the dev
"""

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.dispatcher import run_async

from maindoomer.helpers import check_if_dev
from maindoomer.initdata import BOT
from maindoomer.initdata import LOGGER


@run_async
@check_if_dev
def getlogs(update: Update, context: CallbackContext):
    """Get the bot logs"""
    import datetime
    try:
        # Get the filename
        filename = datetime.date.today().isoformat()
        # Send the file
        BOT.send_document(chat_id=update.effective_chat.id,
                          document=open('logs.log', 'rb'),
                          filename=f'{filename}.log')
    except (EOFError, FileNotFoundError) as changelog_err:
        LOGGER.error(changelog_err)
        BOT.send_message(chat_id=update.effective_chat.id,
                         reply_to_message_id=update.effective_message.message_id,
                         text='Не смог добраться до логов. Что-то не так.')
    finally:
        # Clean the file after sending/create a new one if failed to get it
        with open('logs.log', 'w') as logfile:
            logfile.write(
                f'{datetime.datetime.now().isoformat()} - Start of the log file.\n')


@run_async
@check_if_dev
def sql(update: Update, context: CallbackContext):
    """Use sql commands for the database"""
    from maindoomer import sqlcommands
    statement = ' '.join(update.effective_message.text.split()[1:])
    sqlcommands.run_query(statement)


@run_async
@check_if_dev
def getdatabase(update: Update, context: CallbackContext):
    """Get the database as a document"""
    try:
        # Send the file
        from constants import DATABASENAME
        BOT.send_document(chat_id=update.effective_chat.id,
                          document=open(DATABASENAME, 'rb'))
    except (EOFError, FileNotFoundError) as database_err:
        LOGGER.error(database_err)
        BOT.send_message(chat_id=update.effective_chat.id,
                         reply_to_message_id=update.effective_message.message_id,
                         text='Не смог добраться до датабазы. Что-то не так.')


@run_async
@check_if_dev
def allcommands(update: Update, context: CallbackContext):
    """Send the list of all commands"""
    from thebot import USERCOMMANDS, ONLYADMINCOMMANDS, UNUSUALCOMMANDS
    text = ''
    for commandlists in (USERCOMMANDS, ONLYADMINCOMMANDS, UNUSUALCOMMANDS):
        text += f'<b>{commandlists[0]}:</b>\n'
        for commands in commandlists[1:]:
            text += f'/{commands[0]} - {commands[2]};\n'
    BOT.send_message(chat_id=update.effective_chat.id,
                     reply_to_message_id=update.effective_message.message_id,
                     text=text,
                     parse_mode='HTML')