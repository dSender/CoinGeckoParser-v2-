from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView
import json
from django.conf import settings
from .models import Platform, Market, OnePairArbitrage
import time


class OnePairArbitrageView(FormView):
    template_name = 'one_pair_table.html'
    last_update = time.time()

    def get(self, request, *args, **kwargs):
        file = settings.API_FILE
        data = json.load(open(file, 'r'))
        for platform, arcoins in data.items():
            if time.time() - self.last_update < 60:
                break
            try:
                p = Platform.objects.get(name=platform)
            except Platform.DoesNotExist:
                p = Platform.objects.create(name=platform)
            for arcoin in arcoins:
                name = arcoin[0]
                arbits = arcoin[1]
                for a in arbits:
                    precent = a['precent']
                    baseFrom = a['baseFrom']
                    targetFrom = a['targetFrom']
                    baseTo = a['baseTo']
                    targetTo = a['targetTo']
                    marketFrom = Market.custom_manager.get_or_create(name=a['from'])
                    marketTo = Market.custom_manager.get_or_create(name=a['to'])
                    convertedPriceFrom = a['convertedPriceFrom']
                    convertedPriceTo = a['convertedPriceTo']
                    volume = a['volume']
                    id_ = a['id']

                    opa = OnePairArbitrage.custom_manager.get_or_create(precent=precent, baseFrom=baseFrom, targetFrom=targetFrom,
                                                    baseTo=baseTo, targetTo=targetTo, marketFrom=marketFrom,
                                                    marketTo=marketTo, convertedPriceTo=convertedPriceTo,
                                                    convertedPriceFrom=convertedPriceFrom, volume=volume, aid=id_)
                    opa.platforms.add(p)
            self.last_update = time.time()
        arbits = OnePairArbitrage.custom_manager.all()
        return render(request, self.template_name, {'data': arbits})
