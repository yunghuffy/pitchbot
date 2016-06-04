import urllib3
from slackbot.bot import respond_to
import re
import json
import datetime
from pytz import timezone

gd_base_url = 'http://gd2.mlb.com/'

http = urllib3.PoolManager()
def get_scoreboard(scoreboard_endpoint):
    # Return a dictionary from the json
    # in the master scoreboard
    r = http.request('GET', gd_base_url + scoreboard_endpoint)
    scoreboard = json.loads(r.data)
    return scoreboard

def get_game(team, scoreboard):
    # Look in the scoreboard for the right game
    for i in scoreboard['data']['games']['game']:
        if i[u'home_name_abbrev'] == team or i[u'away_name_abbrev'] == team:
            return i[u'game_data_directory']

def pretty_line_score(game_data):
    req = http.request('GET', '{}{}/linescore.json'.format(gd_base_url, game_data))
    linescore = json.loads(req.data)
    game_status = linescore['data']['game']['status']
    away_abbrev = linescore['data']['game']['away_name_abbrev']
    home_abbrev = linescore['data']['game']['home_name_abbrev']
    if game_status == 'Preview':
        game_time = linescore['data']['game']['time']
        game_zone = linescore['data']['game']['time_zone']
        home_prob = linescore['data']['game']['home_probable_pitcher']
        away_prob = linescore['data']['game']['away_probable_pitcher']
        home_pitch_name = home_prob['last']
        home_era = home_prob['era']
        away_pitch_name = away_prob['last']
        away_era = away_prob['era']
        pre_message = """{:s} at {:s}
Game time - {:s}{:s}
Probables: {:s} (ERA {:s}) vs. {:s} (ERA {:s})"""
        message = pre_message.format(
                away_abbrev,
                home_abbrev,
                game_time,
                game_zone,
                away_pitch_name,
                away_era,
                home_pitch_name,
                home_era)
    elif game_status == 'In Progress':
        away_runs = linescore['data']['game']['away_team_runs']
        home_runs = linescore['data']['game']['home_team_runs']
        inning = linescore['data']['game']['inning']
        is_top = linescore['data']['game']['top_inning']
        outs = linescore['data']['game']['outs']
        runners_on = linescore['data']['game']['runner_on_base_status']
        if is_top == 'Y':
            top_bot = 'Top'
        else:
            top_bot = 'Bottom'
        pre_message = """{:s} ({:s}) at {:s} ({:s})
{:s} {:s}
{:s} outs, {:s} on"""
        message = pre_message.format(
                away_abbrev,
                away_runs,
                home_abbrev,
                home_runs,
                top_bot,
                inning,
                outs,
                runners_on)
    else:
        away_runs = linescore['data']['game']['away_team_runs']
        home_runs = linescore['data']['game']['home_team_runs']
        message = '{:s} ({:s}) at {:s} ({:s})\nStatus: {:s}'.format(
                away_abbrev,
                away_runs,
                home_abbrev,
                home_runs,
                game_status
                )
    return message

@respond_to('score', re.IGNORECASE)
def scoreboard(message):
    #Get today's date for use later
    d = datetime.datetime.now(timezone('US/Eastern'))
    _year = d.strftime("%Y")
    _month = d.strftime("%m")
    _day = d.strftime("%d")
    scoreboard_endpoint = 'components/game/mlb/year_' + _year + \
            '/month_' + _month + \
            '/day_' + _day + \
            '/master_scoreboard.json'
    score = pretty_line_score(get_game('WSH', get_scoreboard(scoreboard_endpoint)))
    message.reply(score)
