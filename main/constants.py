"""Collection of constants for modules."""

# Admin id
# Add developer ID for passing the spam check and other commands
DEVS = [255295801, 205762941]
# Add a ping channel
PING_CHANNEL = -353404420

# Duel constants
# Maximum STR the bot can roll
THRESHOLDCAP = 80
# Low and high accuracy that the user can get without exp
LOW_BASE_ACCURACY = 40
HIGH_BASE_ACCURACY = 50
# Exp multiplier for kills, deaths and misses
KILLMULT = 0.37
DEATHMULT = -0.13
MISSMULT = -0.06
# Always lose percent
ALWAYSLOSS = 0.05
HARDRESETCHANCE = 0.0025  # 0.25%

# DO NOT TOUCH
# -----------------------------------------------------------
# Get the kill, death multiplier and their percentage to total
DATABASE_NAME = 'doomer.db'
KILLMULTPERC = round(KILLMULT / THRESHOLDCAP * 100, 2)
DEATHMULTPERC = round(DEATHMULT / THRESHOLDCAP * 100, 2)
MISSMULTPERC = round(MISSMULT / THRESHOLDCAP * 100, 2)
# Get the HARDCAP to additional strength
STRENGTHCAP = THRESHOLDCAP * (1 - ALWAYSLOSS)
ADDITIONALSTRCAP = STRENGTHCAP - LOW_BASE_ACCURACY
ADDITIONALPERCENTCAP = round(ADDITIONALSTRCAP / THRESHOLDCAP * 100, 2)
# Create dict with all duel data
DUELDICT = {
    'LOW_BASE_ACCURACY': LOW_BASE_ACCURACY,
    'HIGH_BASE_ACCURACY': HIGH_BASE_ACCURACY,
    'KILLMULT': KILLMULT,
    'DEATHMULT': DEATHMULT,
    'MISSMULT': MISSMULT,
    'STRENGTHCAP': STRENGTHCAP,
    'KILLMULTPERC': KILLMULTPERC,
    'DEATHMULTPERC': DEATHMULTPERC,
    'MISSMULTPERC': MISSMULTPERC,
    'ADDITIONALPERCENTCAP': ADDITIONALPERCENTCAP
}
# -----------------------------------------------------------

# Antispam constants
# Delays in seconds for the BOT
INDIVIDUAL_USER_DELAY = 10 * 60  # Ten minutes
# Duel cooldowns
CDREDUCTION = round(0.7 * INDIVIDUAL_USER_DELAY)  # 70%
SHORTCD = round(INDIVIDUAL_USER_DELAY - CDREDUCTION)

# Request timeout time in seconds
REQUEST_TIMEOUT = 3
