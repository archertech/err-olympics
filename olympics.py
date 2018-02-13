
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from errbot import botcmd, BotPlugin


class Olympics(BotPlugin):

    RESULT_TABLE_CLASS = 'ResTableFull'
    MEDALS_URL = 'https://www.pyeongchang2018.com/en/game-time/results/OWG2018/en/general/medal-standings.htm'

    CACHE_LENGTH = 300
    CACHE_EXPIRES = None
    CACHED_MEDALS_PAGE = None

    def activate(self):
        super(Olympics, self).activate()


    def _load_medals_page(self):
        current_time = datetime.datetime.utcnow().timestamp()
        if not self.CACHE_EXPIRES or not self.CACHED_MEDALS_PAGE or self.CACHE_EXPIRES <= current_time:
            response = requests.get(self.MEDALS_URL)
            self.CACHED_MEDALS_PAGE = response.content
            self.CACHE_EXPIRES = (current_time + self.CACHE_LENGTH)


    @botcmd
    def medals(self, msg, args):

        self._load_medals_page()
        soup = BeautifulSoup(self.CACHED_MEDALS_PAGE, 'html.parser')
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
