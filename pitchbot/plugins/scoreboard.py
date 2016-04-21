import mlbgame
from slackbot.bot import respond_to
import re
import datetime
from pytz import timezone

@respond_to('score', re.IGNORECASE)
def scoreboard(message):
    d = datetime.datetime.now(timezone('US/Eastern'))
    year = int(d.strftime("%Y"))
    month = int(d.strftime("%m"))
    day = int(d.strftime("%d"))
    game = mlbgame.day(year, month, day, home="Nationals", away="Nationals")
    my_game = game[0]
    score = my_game.nice_score()
    message.reply(score)
