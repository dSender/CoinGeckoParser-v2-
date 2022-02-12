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
            name = re.sub(r' ', '', name)
            name = name.split(',')
        else:
            return []
        return name

    def get(self, request, *args, **kwargs):
        file = settings.API_FILE
        markets_list_file = settings.MARKETS_FILE
        try:
            data = json.load(open(file, 'r'))
            markets_list = json.load(open(markets_list_file, 'r')).get('Markets')
        except json.JSONDecodeError:
            return HttpResponse('No data available')
        form = self.form_class
        if request.GET:
            get_ = request.GET
            form = form(get_)
            filter_data = dict()
            name = self.cleaned_filter_name(name=get_.get('name'))
            precent = get_.get('precent')
            volume = get_.get('volume')
            checked_markets = get_.get('only_checked_markets')
            print(checked_markets)
            try:
                markets = get_.get('markets').split('/')[1:]
            except AttributeError:
                markets = None

            if precent is not None and precent != '':
                precent = float(precent)

            if volume is not None and volume != '':
                volume = int(volume)

            for d, c in data.items():
                inds = []
                inds_arbits = []
                for i in range(len(c)):
                    if c[i][0] not in name and name != []:
                        inds.append(i)
                    if precent is not None and precent != '' or volume is not None and volume != '' or markets is not None and markets != []:
                        for m in range(len(c[i][1])):
                            if precent is not None and precent != '':
                                if c[i][1][m]['precent'] < precent:
                                    inds_arbits.append([i, m])
                                    continue
                            if volume is not None and volume != '':
                                if c[i][1][m]['volume'] < volume:
                                    inds_arbits.append([i, m])
                                    continue
                            if markets is not None and markets != []:
                                f, t = c[i][1][m]['from'] not in markets, c[i][1][m]['to'] not in markets
                                if (f or t) and checked_markets == 'on':
                                    inds_arbits.append([i, m])
                                elif (f and t) and checked_markets is None:
                                    inds_arbits.append([i, m])
                if inds_arbits:
                    for i in inds_arbits[::-1]:
                        c[i[0]][1].pop(i[1])
                if inds:
                    for i in inds[::-1]:
                        c.pop(i)
        d_keys = list()
        for k, v in data.items():
            f = False
            for i in data[k]:
                if len(i[1]) != 0:
                    f = True
                    break
            if not f:
                d_keys.append(k)
        for i in d_keys:
            data.pop(i)


        return render(request, self.template_name, {'data': data, 'form': form, 'markets_list': markets_list})
