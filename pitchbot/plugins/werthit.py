from slackbot.bot import respond_to
import re
import urllib3
import xml.etree.ElementTree as ET
import locale

@respond_to('Werth', re.IGNORECASE)
def werthit(message):
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://gd2.mlb.com/components/game/mlb/year_2016/batters/150029.xml')
    root = ET.fromstring(r.data)
    hrs = float(root.attrib['s_hr'])
    total_salary = float(21000000)
    games = get_standings()
    season_pct = games / 162.0
    salary = total_salary * season_pct
    locale.setlocale( locale.LC_ALL, '' )
    hrs_per = salary / hrs
    how_much = locale.currency( hrs_per, grouping=True )
    really = "Jayson Werth is being paid %s per home run this year!" % how_much
    message.reply(really)

# oh god please don't look
# ridiculous function just to get standings
def get_standings():
    http = urllib3.PoolManager()
    d = http.request('GET', 'http://espn.go.com/mlb/team/_/name/wsh')
    divs = d.data.split("div")
    for div in divs:
        if "mlb:teamclubhouse:standings:team\" href=\"/mlb/team/_/name/wsh" in div:
            cols = div.split('td class="right"')
    base_col = [z for z,x in enumerate(cols) if "Washington" in x][0]
    windex = base_col + 1
    lossdex = base_col + 2
    wins = cols[windex].lstrip('>').split('<')[0]
    losses = cols[lossdex].lstrip('>').split('<')[0]
    total_games = int(wins) + int(losses)
    return total_games
