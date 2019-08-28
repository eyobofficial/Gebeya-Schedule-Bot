welcome_message = \
"""
Hi {}! You are currently enrolled to the {} track \
during the {}-time session. Checkout your class schedules using the \
following commands:
/today - for your today class schedules
/tomorrow - for your tomorrow class schedules
/week - for your one week class schedules
/month - for your one month class schedules

To change your track or session, use the following commands:
/track - for setting your track
/session - for setting your session
/me - to see your current track and session

For more commands:
/help - for getting the list of all commands
/credits - for meeting the developers
"""


help_message = \
"""
*Class Schedules*
/today - get today class schedules
/tomorrow - get tomorrow class schedules
/week - get class schedules for 1 week from today
/month - get class schedules for 1 week from today

*Account Settings*
/track - set or change your track
/session - set or change your class session

*Help*
/help - get the list of all commands
/about - get overview about the bot.
/credits - get the list of contributors.
"""

session_missing = \
"""
But I don't know your class session yet. Use the /session command to set it.
"""

track_missing = \
"""
But I don't know your track yet. Use the /track command to set it.
"""


me = \
"""
*Name:* {}

*Track:* {}

*Session: *{}

You can update your track and session using the /track & /session commands.
"""
