"""/pidor command."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, run_async
from telegram.error import BadRequest

from main import randomizer
from main.database import *
from main.constants import DEVS
from main.helpers import antispam_passed, check_if_group_chat, ResetError


@run_async
@antispam_passed
@check_if_group_chat
@db_session
def pidor(update: Update, context: CallbackContext):
    """Get the pidor of the day from all users stored for the chat."""
    # Check if there is already a pidor of the day
    pidor_today = select(q.user_id.full_name for q in Pidors
                         if q.chat_id == Chats[update.message.chat.id]
                         and q.day == date.today())[:][:]
    if pidor_today:
        update.message.reply_text(
            text=f'Пидором дня является {pidor_today[0]}!')
        return
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Реролл #1 (только админы)', callback_data='Reroll.1')]])
    update.message.reply_text(text=f'Пидором дня является {getnew(update).result()}!',
                              parse_mode='Markdown',
                              reply_markup=keyboard)


@run_async
@db_session
def getnew(update: Update) -> str:
    """Look for new pidor."""
    chat_users = select(q.user_id for q in User_Stats
                        if q.chat_id == Chats[update.message.chat.id])[:][:]
    # Find a pidor that's still in the chat and delete those that are gone.
    while chat_users:
        pidor = randomizer.choice(chat_users)
        try:
            pidor_data = update.message.chat.get_member(user_id=pidor.id)
            if pidor_data.status not in ['restricted', 'left', 'kicked'] and \
                    not pidor_data.user.is_bot:
                break
            else:
                delete(u for u in User_Stats
                       if u.user_id == pidor
                       and u.chat_id == Chats[update.message.chat.id])
                chat_users.remove(pidor)
        except BadRequest:
            delete(u for u in User_Stats
                   if u.user_id == pidor
                   and u.chat_id == Chats[update.message.chat.id])
            chat_users.remove(pidor)
    else:
        update.message.reply_text('Нужно больше данных!')
        raise ResetError
    # Assign a tag
    Users[pidor.id].full_name = pidor_data.user.full_name
    pidor_tag = f'[{pidor.full_name}](tg://user?id={pidor.id})'
    if not Pidors.exists(chat_id=Chats[update.message.chat.id]):
        Pidors(chat_id=Chats[update.message.chat.id],
               user_id=pidor,
               day=date.today())
    else:
        Pidors[Chats[update.message.chat.id]].user_id = pidor
        Pidors[Chats[update.message.chat.id]].day = date.today()
    # Record and return
    User_Stats[Users[pidor.id],
               Chats[update.message.chat.id]].times_pidor += 1
    return pidor_tag


@run_async
@db_session
def reroll(update: Update, context: CallbackContext):
    """Reroll pidor of the day."""
    admins = [u.user for u in context.bot.get_chat_administrators(
        update.callback_query.message.chat.id)]
    if update.callback_query.from_user in admins or \
            update.callback_query.from_user.id in DEVS:
        rolln = int(
            update.callback_query.message.reply_markup.inline_keyboard[0][0].callback_data.split('.')[-1]) + 1
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'Реролл #{rolln} (только админы)',
                                   callback_data=f'Reroll.{rolln}')]])
        update.callback_query.message.edit_text(
            text=f'Пидором дня является {getnew(update.callback_query).result()}!',
            parse_mode='Markdown',
            reply_markup=keyboard)
