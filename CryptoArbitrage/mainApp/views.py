from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView
from django.conf import settings
import json



class OnePairArbitrageView(FormView):
    template_name = 'one_pair_table.html'

    def get(self, request, *args, **kwargs):
        file = settings.API_FILE
        data = json.load(open(file, 'r'))
        
        return render(request, self.template_name, {'data': data})
