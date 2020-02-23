"""/duel command."""

from datetime import timedelta
from time import sleep

from telegram import Update, User, Chat
from telegram.ext import CallbackContext, run_async

from commandPretexts.duels import DUELS
from main import randomizer
from main.constants import THRESHOLDCAP, DUELDICT as DD
from main.database import *
from main.helpers import ResetError, antispam_passed, check_if_group_chat


class Dueler:
    """Basic storer for a dueler data."""

    def __init__(self, user: User, chat: Chat):
        """Initiate the dueler instance."""
        self.user = user
        self.chat = chat
        self.tag = f'[{self.user.full_name}](tg://user?id={self.user.id})'

    def duel(self, target) -> None:
        """Duel another dueler and get the outcome."""
        win_req = randomizer.uniform(0, THRESHOLDCAP)
        self.strength, target.strength = self._win_chance(), target._win_chance()
        if self.strength < win_req and target.strength < win_req:
            self.outcome, target.outcome = (0, 0, 1), (0, 0, 1)
        else:
            if self.strength > target.strength:
                self.outcome, target.outcome = (1, 0, 0), (0, 1, 0)
            elif self.strength < target.strength:
                self.outcome, target.outcome = (0, 1, 0), (1, 0, 0)
            elif self.strength == target.strength:
                self.outcome, target.outcome = (1, 1, 0), (1, 1, 0)
        # Record the result
        self._record_result(target)

    @db_session
    def _win_chance(self) -> float:
        """User win chance for the duel."""
        user_stats = User_Stats[Users[self.user.id], Chats[self.chat.id]]
        strength = randomizer.uniform(DD['LOW_BASE_ACCURACY'], DD['HIGH_BASE_ACCURACY']) \
            + user_stats.kills * DD['KILLMULT'] \
            + user_stats.deaths * DD['DEATHMULT'] \
            + user_stats.misses * DD['MISSMULT']
        return min(strength, DD['STRENGTHCAP'])

    @db_session
    def _record_result(self, target) -> None:
        """Record the duel result."""
        for dueler in (self, target):
            user_stats = User_Stats[Users[dueler.user.id],
                                    Chats[dueler.chat.id]]
            user_stats.kills += dueler.outcome[0]
            user_stats.deaths += dueler.outcome[1]
            user_stats.misses += dueler.outcome[2]


@run_async
@check_if_group_chat
@antispam_passed
@db_session
def duel(update: Update, context: CallbackContext) -> None:
    """Duel to solve any kind of argument."""
    # Check if the duels are activated for the chat
    if not Options[Chats[update.message.chat.id]].duel_active:
        update.message.reply_text('Дуэли отключены.')
        raise ResetError
    # Check if a target was selected
    if update.message.reply_to_message is None:
        reply = ('С кем дуэль проводить будем?\n'
                 'Чтобы подуэлиться, надо чтобы вы ответили вашему оппоненту.')
        update.message.reply_text(reply)
        raise ResetError
    try_to_duel(update, context)


@run_async
def try_to_duel(update: Update, context: CallbackContext) -> None:
    """Try to duel. Main duel function."""
    # Shorten the code, format the names
    init = Dueler(update.message.from_user,
                  update.message.chat)
    target = Dueler(update.message.reply_to_message.from_user,
                    update.message.chat)
    # Tree for when the target is not self
    if target.user.id == context.bot.id:
        update.message.reply_text(randomizer.choice(DUELS['bot']))
    elif target.user.id == init.user.id:
        update.message.reply_text(randomizer.choice(DUELS['suicide']))
    else:
        init.duel(target)
        result = use_names(init, target).result()
        conclude(update, context, result)


@run_async
def use_names(init: Dueler, target: Dueler) -> str:
    """Insert names into the strings."""
    if init.outcome == (1, 1, 0):
        reply = randomizer.choice(DUELS['alldead']).replace(
            'winner1', init.tag).replace('winner2', target.tag)
    elif init.outcome == (1, 0, 0):
        reply = randomizer.choice(DUELS['onedead']).replace(
            'winner', init.tag).replace('loser', target.tag)
        reply += f'\nПобеда за {init.tag}!'
    elif init.outcome == (0, 1, 0):
        reply = randomizer.choice(DUELS['onedead']).replace(
            'winner', target.tag).replace('loser', init.tag)
        reply += f'\nПобеда за {target.tag}!'
    elif init.outcome == (0, 0, 1):
        reply = randomizer.choice(DUELS['nonedead']).replace(
            'loser1', init.tag).replace('loser2', target.tag)
    return reply


@run_async
def conclude(update: Update, context: CallbackContext, result: str) -> None:
    """Send all the messages for the duel."""
    # Send the initial message
    botmsg = update.message.reply_text('Дуэлисты расходятся...')
    # Make the message loop
    for phrase in ('Готовятся к выстрелу...', '***BANG BANG***', result):
        sleep(0.85)
        botmsg = context.bot.edit_message_text(
            chat_id=update.message.chat.id,
            text=phrase,
            message_id=botmsg.message_id,
            parse_mode='Markdown'
        )
