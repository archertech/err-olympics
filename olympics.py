
import logging
import requests
from bs4 import BeautifulSoup
from errbot import botcmd, BotPlugin


class Olympics(BotPlugin):

    RESULT_TABLE_CLASS = 'ResTableFull'
    MEDALS_URL = 'https://www.pyeongchang2018.com/en/game-time/results/OWG2018/en/general/medal-standings.htm'

    def activate(self):
        super(Olympics, self).activate()


    @botcmd
    def medals(self, msg, args):

        response = requests.get(self.MEDALS_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        results_table = soup.find('table', attrs={'class': self.RESULT_TABLE_CLASS})

        for row in results_table.find_all('tr'):
           cells = row.find_all('td')
           if not cells:
               continue

           rank = cells[0].text.strip()
           country = cells[1].text.strip()
           golds = cells[2].text.strip()
           silvers = cells[3].text.strip()
           bronzes = cells[4].text.strip()

           yield '{} | {} | {} | {} | {}'.format(
               rank.zfill(2),
               country.ljust(20),
               golds.rjust(3),
               silvers.rjust(3),
               bronzes.rjust(3))

        yield 'Source: {}'.format(self.MEDALS_URL)
