from django.db import models
from django.conf import settings


file = settings.API_FILE


class Platform(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Coin(models.Model):
    name = models.CharField(max_length=42)
    symbol = models.CharField(max_length=24)
    platforms = models.ForeignKey(Platform, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class OnePairArbitrage(models.Model):
    precent = models.FloatField()
    baseFrom = models.OneToOneField(Coin, on_delete=models.CASCADE, related_name='baseFrom')
    targetFrom = models.OneToOneField(Coin, on_delete=models.CASCADE, related_name='targetFrom')
    baseTo = models.OneToOneField(Coin, on_delete=models.CASCADE, related_name='baseTo')
    targetTo = models.OneToOneField(Coin, on_delete=models.CASCADE, related_name='targetTo')
    marketFrom = models.OneToOneField(Market, on_delete=models.CASCADE, related_name='marketFrom')
    marketTo = models.OneToOneField(Market, on_delete=models.CASCADE, related_name='marketTo')
    convertedPriceFrom = models.FloatField()
    convertedPriceTo = models.FloatField()
    volume = models.FloatField()
