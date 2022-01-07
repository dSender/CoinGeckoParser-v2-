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
        return render(request, self.template_name, {'data': data})
