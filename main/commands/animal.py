"""/cat and /dog command."""

import requests
import telegram.error
from telegram import Update
from telegram.ext import CallbackContext, run_async

from main.constants import REQUEST_TIMEOUT
from main.helpers import antispam_passed, ResetError


@run_async
@antispam_passed
def animal(update: Update, context: CallbackContext):
    """Get photo/video/gif of dog or cat.

    Raise errors to reset the command cooldown.
    telegram.error.BadRequest is handled by @command_antispam_passed to reset.
    """
    # Cat link
    if '/cat' in update.message.text.lower():
        link = 'http://aws.random.cat/meow'
    # Dog link
    else:
        link = 'https://random.dog/woof.json'
    response = requests.get(url=link, timeout=REQUEST_TIMEOUT)
    if response.status_code != requests.codes.ok:
        update.message.reply_text(
            'Сервер не работает, интересно. Попробуйте позже.')
        # Reset cooldown
        raise ResetError
    # Try to send chat action, check if the bot has the right to send messages
    context.bot.send_chat_action(update.message.chat.id, 'upload_photo')
    file_link = [item for item in response.json().values()
                 if 'http' in str(item)][0]
    file_extension = file_link.split('.')[-1]
    # Try to send it to the chat
    try:
        if 'mp4' in file_extension:
            context.bot.send_video(
                chat_id=update.message.chat.id,
                video=file_link,
                reply_to_message_id=update.message.message_id
            )
        elif 'gif' in file_extension:
            context.bot.send_animation(
                chat_id=update.message.chat.id,
                animation=file_link,
                reply_to_message_id=update.message.message_id
            )
        else:
            context.bot.send_photo(
                chat_id=update.message.chat.id,
                photo=file_link,
                reply_to_message_id=update.message.message_id
            )
    except telegram.error.BadRequest:
        update.message.reply_text(
            'Недостаточно прав для отправки медиа файлов, вопросы к админу.\n'
            'Нужно право на отправку медиа файлов и GIF файлов.')
        # Reset cooldown
        raise telegram.error.BadRequest
