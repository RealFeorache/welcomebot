"""/pidor command."""

from telegram import Update
from telegram.ext import CallbackContext, run_async

from main import randomizer
from main.database import *
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
        update.message.reply_text(f'Пидором дня является {pidor_today[0]}!')
        return
    # Look for new pidor
    chat_users = select(q.user_id for q in User_Stats
                        if q.chat_id == Chats[update.message.chat.id])[:][:]
    # Find a pidor that's still in the chat and delete those that are gone.
    while True:
        if not chat_users:
            update.message.reply_text('Нужно больше данных')
            raise ResetError
        pidor = randomizer.choice(chat_users)
        pidor_data = update.message.chat.get_member(user_id=pidor.id)
        if pidor_data.status in ['restricted', 'left', 'kicked'] or \
                pidor_data.user.is_bot:
            delete(u for u in User_Stats
                   if u.user_id == pidor
                   and u.chat_id == Chats[update.message.chat.id])
            chat_users.remove(pidor)
        else:
            break
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
    # Record and reply
    User_Stats[Users[pidor.id],
               Chats[update.message.chat.id]].times_pidor += 1
    reply = f'Пидором дня является {pidor_tag}!'
    update.message.reply_text(text=reply, parse_mode='Markdown')
