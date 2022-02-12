import requests
import json
import time


class CoinMetaClass:

    '''This class contains all coins instances'''

    instance = list()

    def __init__(self):
        self.instance.append(self)


class Coin(CoinMetaClass):
    name = ''
    fees_url = ''
    symbol = ''

    def __init__(self, name, platforms, tickers, fees_url, symbol, id):
        super().__init__()
        self.name = name
        self.platforms = platforms
        self.tickers = tickers
        self.fees_url = fees_url
        self.symbol = symbol
        self.id = id

    def get_coin_platforms(self):
        return self.platforms

    def get_coin_tickers(self):
        return self.tickers

    def __str__(self):
        return self.name


class Scraper:

    '''Coingecko scraper, using coingecko public API'''

    calls = 0
    total_calls = 0
    def __init__(self, api_calls_limit=49, timeout=60):
        self.api_calls_limit = api_calls_limit
        self.timeout = timeout

    def get_page(self, url):
        self.calls += 1
        if self.calls >= self.api_calls_limit:
            self.total_calls += self.calls
            print('Timeout, total calls %d' % self.total_calls)
            self.calls = 0
            time.sleep(self.timeout)

        while 1:
            try:
                r = requests.get(url, timeout=10)
            except:
                continue
            else:
                if r.status_code == 200:
                    break
        return r

    def get_servers_status(self):
        ping_url = 'https://api.coingecko.com/api/v3/ping'
        return self.get_page(ping_url).status_code

    def get_all_coins(self):

        '''List of all coins in format  Coin name: coin id'''

        coins_url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
        coins = json.loads(self.get_page(coins_url).text)
        clear_data = list()
        for coin in coins:
            if 'short' not in coin['id'] and 'long' not in coin['id']:
                clear_data.append([coin['name'], coin['id'], coin['symbol']])
        return clear_data

    def get_coin_info(self, coin_id, coin_name):

        '''Collects arbitrage important information: platforms/tickers. Returns a list.'''

        coin_url = 'https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false'.format(coin_id)
        coin_data = json.loads(self.get_page(coin_url).text)

        # Gets tickers data: market name, base coin, target coin, price and volume in usd
        tickers = coin_data.get('tickers')
        if len(tickers) < 2:
            return None
        clear_data = list()
        for ticker in tickers:
            market_name = ticker.get('market').get('name')
            base = ticker.get('base').lower()
            target = ticker.get('target').lower()
            converted_price = ticker.get('converted_last').get('usd')
            volume =  ticker.get('converted_volume').get('usd')
            last_price = ticker.get('last')
            clear_data.append({'market': market_name, 'base': base, 'target': target, 'converted price': converted_price, 'volume': volume, 'last_price': last_price})

        # Gets platforms where coin is run
        platforms = coin_data.get('platforms')

        # coin fees url
        slug_name = coin_name.replace(' ', '-')
        fee_url = 'https://withdrawalfees.com/coins/{}'.format(slug_name.lower())
        return [platforms, clear_data, fee_url]
