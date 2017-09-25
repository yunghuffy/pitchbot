from datetime import datetime
from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import urllib3
import xml.etree.ElementTree as ET
import locale
import mlbgame
import re


class WerthItPlugin(MachineBasePlugin):

    @listen_to(regex=r'Werth')
    def werthit(self, msg):
        http = urllib3.PoolManager()
        base_url = 'http://gd2.mlb.com/components/game/mlb/year_'
        now = datetime.now()
        year = datetime.strftime(now, "%Y")
        player_id = '150029'
        player_url = base_url + year + '/batters/' + player_id + '.xml'
        print(player_url)
        r = http.request(
            'GET',
            player_url
        )
        root = ET.fromstring(r.data)
        hrs = float(root.attrib['s_hr'])
        total_salary = float(21000000)
        games = self.get_total_games()
        season_pct = games / 162.0
        salary = total_salary * season_pct
        locale.setlocale(locale.LC_ALL, '')
        hrs_per = salary / hrs
        how_much = locale.currency(hrs_per, grouping=True)
        really = """
        Jayson Werth is being paid {} per home run this year!
        """.format(how_much)
        msg.say(really)

    def get_total_games(self):
        all_teams = []
        for division in mlbgame.standings().divisions:
            all_teams.extend(division.teams)
        for team in all_teams:
            if team.team_abbrev == 'WSH':
                total_games = int(team.l) + int(team.w)
        return total_games
