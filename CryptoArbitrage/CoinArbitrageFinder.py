from CoinGeckoScraper import Scraper, Coin
from pathlib import Path
import json
import time


scraper = Scraper()

arbit_id = -1
def arbitrage_finder_one_pair(tickers, precent=1.009):
    arbits = []
    global arbit_id
    for t in range(len(tickers)):
        m1 = tickers[t].get('market')
        conv_price1 = tickers[t].get('converted price')
        b1 = tickers[t].get('base')
        t1 = tickers[t].get('target')
        volume1 = tickers[t].get('volume')
        for t2 in range(t+1, len(tickers)):
            conv_price2 = tickers[t2].get('converted price')
            if ((conv_price1 / conv_price2 <= precent) and (conv_price1 >= conv_price2)) or ((conv_price2 / conv_price1) <= precent and conv_price2 >= conv_price1):
                continue
            b2 = tickers[t2].get('base')
            t_2 = tickers[t2].get('target')
            m2 = tickers[t2].get('market')
            volume2 = tickers[t2].get('volume')
            if b1 not in (t_2, b2) or t1 not in (t_2, b2):
                continue

            fees = list()
            for i in coins:
                if i.symbol in (t_2, b2):
                    fees.append(i.fees_url)
            arbit_id += 1
            if conv_price1 > conv_price2:
                p = ((conv_price1 / conv_price2) - 1) * 100
                arbits.append({'precent': int(p),
                'from': m2, 'to': m1,
                'baseFrom': b2, 'targetFrom': t_2,
                'baseTo': b1, 'targetTo': t1,
                'convertedPriceFrom': conv_price2, 'convertedPriceTo': conv_price1,
                'volume': min(volume1, volume2), 'id': arbit_id,
                'fees': fees})
            else:
                p = ((conv_price2 / conv_price1) - 1) * 100
                arbits.append({'precent': int(p),
                'from': m1, 'to': m2,
                'baseFrom': b1, 'targetFrom': t1,
                'baseTo': b2, 'targetTo': t_2,
                'convertedPriceFrom': conv_price1, 'convertedPriceTo': conv_price2,
                'volume': min(volume1, volume2), 'id': arbit_id,
                'fees': fees})
    return arbits


def arbit_func(coins):
    with open('onePairCoinArbit.json', 'w+') as file:
        js = dict()
        for coin in coins:
            tic = coin.get_coin_tickers()
            arbitData = arbitrage_finder_one_pair(tic)
            if arbitData == []:
                continue
            platforms = coin.get_coin_platforms()
            for k in platforms.keys():
                if k not in js.keys():
                    js[k] = [[coin.name, arbitData]]
                else:
                    js[k].append([coin.name, arbitData])
        json.dump(js, file)

w = 0

def convert_tickers_contracts():
    coins = Coin.__base__.instance
    for cc in coins:
        tickers = cc.get_coin_tickers()
        for t in tickers:
            if len(t['base']) == 42:
                for c in coins:
                    ct = c.get_coin_platforms().values()
                    if t['base'] in ct:
                        t['base'] = c.symbol
            if len(t['target']) == 42:
                for c in coins:
                    ct = c.get_coin_platforms().values()
                    if t['target'] in ct:
                        t['target'] = c.symbol
        cc.tickers = tickers


if scraper.get_servers_status() == 200:
    coins = scraper.get_all_coins()
    for coin in coins:
        if scraper.calls == 49:
            coins = Coin.__base__.instance
            arbit_func(coins)
        w+=1
        if w == 5000:
            break
        name, id, symbol = coin[0], coin[1], coin[2]
        data = scraper.get_coin_info(id, name)
        if data == None:
            continue
        platforms, tickers, fees_url = data
        convert_tickers_contracts()
        Coin(name, platforms, tickers, fees_url, symbol)
