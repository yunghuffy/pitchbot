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
    salary = float(21000000)
    locale.setlocale( locale.LC_ALL, '' )
    hrs_per = salary / hrs
    how_much = locale.currency( hrs_per, grouping=True )
    really = "Jayson Werth is being paid %s per home run this year!" % how_much
    message.reply(really)
