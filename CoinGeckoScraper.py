import requests
import json


class CoinMetaClass:

    '''This class contains all coins instances'''

    instance = list()

    def __init__(self):
        self.instance.append(self)

    def instance_len(self):
        return len(self.instance)


class Coin(CoinMetaClass):
    def __init__(self, name, platforms=dict(), tickers=list()):
        super().__init__()
        self.name = name
        self.platforms = platforms
        self.tickers = tickers

    def get_coin_platforms(self):
        return self.platforms

    def get_coin_tickers(self):
        return self.tickers

    def __str__(self):
        return self.name


class Scraper:

    '''Coingecko scraper, using coingecko public API'''

    def get_servers_status(self):
        ping_url = 'https://api.coingecko.com/api/v3/ping'
        return requests.get(ping_url).status_code

    def get_all_coins(self):

        '''List of all coins in format  Coin name: coin id'''

        coins_url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
        coins = json.loads(requests.get(coins_url).text)
        clear_data = list()
        for coin in coins:
            if 'short' not in coin['id'] and 'long' not in coin['id']:
                clear_data.append([coin['name'], coin['id']])
        return clear_data

    def get_coin_info(self, coin_id):

        '''Collects arbitrage important information: platforms/tickers. Returns a list.'''

        coin_url = 'https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false'.format(coin_id)
        coin_data = json.loads(requests.get(coin_url).text)

        # Gets tickers data: market name, base coin, target coin, price and volume in usd
        tickers = coin_data.get('tickers')
        if len(tickers) < 2:
            return None
        clear_data = list()
        for ticker in tickers:
            market_name = ticker.get('market').get('name')
            base = ticker.get('base')
            target = ticker.get('target')
            converted_price = ticker.get('converted_last').get('usd')
            volume =  ticker.get('converted_volume').get('usd')
            clear_data.append({'market': market_name, 'base': base, 'target': target, 'converted price': converted_price, 'volume': volume})

        # Gets platforms where coin is run
        platforms = coin_data.get('platforms')
        return [platforms, clear_data]


s = Scraper()
coins = s.get_all_coins()
w = 0
while w != 20:
    coin_name, coin_id = coins[w][0], coins[w][1]
    w += 1
    data = s.get_coin_info(coin_id)
    if data is not None:
        platforms, tickers = data
        Coin(coin_name, platforms, tickers)

meta = CoinMetaClass()
print(meta.instance_len())

for i in range(15):
    print(meta.instance[i])
