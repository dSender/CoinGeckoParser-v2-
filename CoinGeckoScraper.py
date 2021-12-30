import requests
import json


class Coin:
    def __init__(self, name, platforms=dict(), tickers=list()):
        self.name = name
        self.platforms = platforms
        self.tickers = tickers

    def get_arbitrage_situations(self):

        '''The keys are market data where price is lower'''

        arbit = list()
        for i in range(0, len(self.tickers)-1):
            base = self.tickers[i]['base']
            target = self.tickers[i]['target']
            price = self.tickers[i]['converted price']
            for k in range(i, len(self.tickers)-1):
                sbase = self.tickers[k]['base']
                starget = self.tickers[k]['target']
                pare = [sbase, starget]
                if base in pare and target in pare:
                    sprice = self.tickers[k]['converted price']
                    market = self.tickers[i]['market']
                    smarket = self.tickers[k]['market']
                    precent = 0
                    if sprice > price:
                        precent = sprice / price
                    else:
                        precent = price / sprice
                        tmpb = base
                        tmpt = target
                        base, target = sbase, starget
                        sbase, starget = tmpb, tmpt
                        market, smarket = smarket, market
                        price, sprice = sprice, price
                    if precent > 1:
                        arbit.append([precent, {'{}/{}'.format(base, target): '{}/{}'.format(sbase, starget), price: sprice, market: smarket}])
        return arbit

    def get_coin_platforms(self):
        return self.platforms

    def __str__(self):
        return self.name


class Scraper:

    '''Coingecko scraper, using coingecko public API'''

    def get_servers_status(self):
        ping_url = 'https://api.coingecko.com/api/v3/ping'
        return requests.get(ping_url).status_code

    def get_json_page(self, url):
        return json.loads(requests.get(url).text)

    def get_all_coins(self):

        '''List of all coins in format  Coin name: coin id'''

        coins_url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
        coins = self.get_json_page(coins_url)
        clear_data = list()
        for coin in coins:
            if 'short' not in coin['id'] and 'long' not in coin['id']:
                clear_data.append({coin['name']:coin['id']})
        return clear_data

    def get_coin_platforms(self, coin_id):
        coin_url = 'https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'.format(coin_id)
        coin_data = self.get_json_page(coin_url)
        platforms = coin_data.get('platforms')
        return platforms

    def get_coin_tickers(self, coin_id):

        '''Coin tickers, includes market name, base coin, target coin, converted price to usd, volume in usd'''

        coin_url = 'https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false'.format(coin_id)
        coin_data = self.get_json_page(coin_url)
        tickers = coin_data.get('tickers')
        clear_data = list()
        for ticker in tickers:
            market_name = ticker.get('market').get('name')
            base = ticker.get('base')
            target = ticker.get('target')
            converted_price = ticker.get('converted_last').get('usd')
            volume =  ticker.get('converted_volume').get('usd')
            clear_data.append({'market': market_name, 'base': base, 'target': target, 'converted price': converted_price, 'volume': volume})
        return clear_data


tickers = Scraper().get_coin_tickers('pancakeswap-token')
platforms = Scraper().get_coin_platforms('pancakeswap-token')
coin = Coin('Cake', platforms, tickers)
arbits = coin.get_arbitrage_situations()
print(coin.__str__())
for i in arbits:
    if i[0] > 1.005:
        print(i)
