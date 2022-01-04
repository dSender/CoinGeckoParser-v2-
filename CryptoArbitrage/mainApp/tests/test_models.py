from django.test import TestCase
from mainApp.models import Platform, Coin, Market, OnePairArbitrage


class TestModels(TestCase):

    def setUp(self):
        self.p = Platform.objects.create(name='ethereum')
        self.c = Coin.objects.create(name='bitcoin', symbol='btc', platforms=self.p)
        self.m1 = Market.objects.create(name='Binance')
        self.m2 = Market.objects.create(name='MEXC')

        self.arbit = OnePairArbitrage.objects.create(
            percent=1.01,
            baseFrom=self.p,
            targetFrom=self.c,
            baseTo=self.p,
            targetTo=self.c,
            marketFrom=self.m1,
            marketTo=self.m2,
            convertedPriceFrom=1,
            convertedPriceTo=1.01,
            volume=2.23
        )
