"""/duelranking command."""

from telegram import Update
from telegram.ext import CallbackContext, run_async

from main.database import *
from main.helpers import ResetError, antispam_passed, check_if_group_chat


@run_async
@check_if_group_chat
@antispam_passed
@db_session
def duelranking(update: Update, context: CallbackContext):
    """Get the top best duelists."""

    query = select(q for q in User_Stats
                   if q.chat_id == Chats[update.message.chat.id]
                   ).order_by(
        lambda: desc(q.kills*3+q.deaths*2+q.misses*1))[:10]
    # Check if the chat table exists
    if not query:
        update.message.reply_text('Для этого чата нет данных.')
        raise ResetError

    reply = '***Имя - Убийства/Смерти/Промахи (топ 10)\n***'
    reply += '\n'.join(
        [f'#{c[0]} {c[1].user_id.full_name} - {c[1].kills}/{c[1].deaths}/{c[1].misses}' for c in enumerate(query, 1)])
    update.message.reply_text(text=reply, parse_mode='Markdown')
