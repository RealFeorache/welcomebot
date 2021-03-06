"""/flip command."""

from telegram import Update
from telegram.ext import CallbackContext, run_async

from main import randomizer
from main.helpers import antispam_passed


@run_async
@antispam_passed
def flip(update: Update, context: CallbackContext):
    """Flip a coin."""
    update.message.reply_text(randomizer.choice(['Орёл!', 'Решка!']))
