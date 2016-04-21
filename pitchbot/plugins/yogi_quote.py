from slackbot.bot import respond_to
from pitchbot.data.yogi_quote import quotes
import random
import re

@respond_to('Yogi me', re.IGNORECASE)
def yogi(message):
    yogi_quote = quotes[random.randrange(0,49)]
    message.reply(yogi_quote)
