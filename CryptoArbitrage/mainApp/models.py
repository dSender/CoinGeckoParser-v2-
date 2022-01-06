from django.db import models, IntegrityError



class CustomManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        try:
            return self.get(**kwargs)
        except:
            return self.create(**kwargs)


class CustomArbitManager(models.Manager):
    def delete_on_create(self, *args, **kwargs):
        try:
            return self.get(**kwargs)
        except:
            try:
                return self.create(**kwargs)
            except IntegrityError:
                self.get(**kwargs).delete()
                return self.create(**kwargs)


class Platform(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=32)
    custom_manager = CustomManager()


    def __str__(self):
        return self.name

class OnePairArbitrage(models.Model):
    aid = models.IntegerField(unique=True)
    precent = models.FloatField()
    baseFrom = models.CharField(max_length=42)
    targetFrom = models.CharField(max_length=42)
    baseTo = models.CharField(max_length=42)
    targetTo = models.CharField(max_length=42)
    marketFrom = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='marketFrom')
    marketTo = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='marketTo')
    platforms = models.ManyToManyField(Platform)
    convertedPriceFrom = models.FloatField()
    convertedPriceTo = models.FloatField()
    volume = models.FloatField()
    custom_manager = CustomArbitManager()

    def __str__(self):
        return '{}'.format(self.aid)
