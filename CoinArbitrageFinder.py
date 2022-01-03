from CoinGeckoScraper import Scraper, Coin
import json
import time


scraper = Scraper()


def arbitrage_finder_one_pair(tickers, precent=1.00):
    arbits = []
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
            if conv_price1 > conv_price2:
                p = conv_price1 / conv_price2
                arbits.append({'precent': p,
                'from': m2, 'to': m1,
                'baseFrom': b2, 'targetFrom': t_2,
                'baseTo': b1, 'targetTo': t1,
                'convertedPriceFrom': conv_price2, 'convertedPriceTo': conv_price1,
                'volume': min(volume1, volume2)})
            else:
                p = conv_price2 / conv_price1
                arbits.append({'precent': p,
                'from': m1, 'to': m2,
                'baseFrom': b1, 'targetFrom': t1,
                'baseTo': b2, 'targetTo': t_2,
                'convertedPriceFrom': conv_price1, 'convertedPriceTo': conv_price2,
                min(volume1, volume2)})
    return arbits


def arbit_func(coins):
    with open('onePairCoinArbit.json', 'w+') as file:
        js = dict()
        for coin in coins:
            tic = coin.get_coin_tickers()
            try:
                arbitData = arbitrage_finder_one_pair(tic)
            except:
                continue
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
if scraper.get_servers_status() == 200:
    coins = scraper.get_all_coins()
    for coin in coins[::-1]:
        w+=1
        if w == 10000:
            break
        name, id = coin[0], coin[1]
        data = scraper.get_coin_info(id)
        if data == None:
            continue
        platforms, tickers = data
        Coin(name, platforms, tickers)
        if scraper.calls == 49:
            coins = Coin.__base__.instance
            arbit_func(coins)
