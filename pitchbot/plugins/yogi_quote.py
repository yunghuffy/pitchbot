from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
from pitchbot.data.yogi_quote import quotes
import random
import re


class YogiQuote(MachineBasePlugin):

    @listen_to(regex=r'(Y|y)ogi')
    def yogi(self, message):
        yogi_quote = quotes[random.randrange(0, 49)]
        message.reply(yogi_quote)
