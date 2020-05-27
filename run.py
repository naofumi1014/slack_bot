# -*- coding: utf-8 -*-

from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message(
        '**********',               #channel
        '**********',               #message
        username = '*********',     #name of bot
        icon_emoji = '********'     #name of icon
    )

    main()
    