from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
import json
from django.conf import settings
from .models import Platform, Market, OnePairArbitrage
import time
from .forms import FilterForm
import re


class OnePairArbitrageView(FormView):
    template_name = 'one_pair_table.html'
    last_update = time.time()
    form_class = FilterForm

    def cleaned_filter_name(self, *args, **kwargs):
        cl_data = dict()
        name = kwargs.get('name')
        if name is not None and name != '':
            name = re.split(r'[, ]', name)
        else:
            return []
        return name

    def get(self, request, *args, **kwargs):
        file = settings.API_FILE
        data = json.load(open(file, 'r'))
        form = self.form_class
        if request.GET:
            get_ = request.GET
            form = form(get_)
            filter_data = dict()
            name = self.cleaned_filter_name(name=get_.get('name'))
            print(name)
            for d, c in data.items():
                inds = []
                for i in range(len(c)):
                    if c[i][0] not in name and name != []:
                        inds.append(i)
                if inds:
                    for i in inds[::-1]:
                        c.pop(i)

        return render(request, self.template_name, {'data': data, 'form': form})
