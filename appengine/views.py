from google.appengine.api import users
from google.appengine.ext import webapp

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson 
from operator import itemgetter
from google.appengine.ext.webapp import util, template

import os
import sys

def MainView(request):
    cod = request.GET.get('cod', '')
    values = retrieveValues(cod)
    path = os.path.join(os.path.dirname(__file__), 'templates/beautiful.html')
    html = template.render(path, values)
    return HttpResponse(html) ## or

def PacView(request):
    cod = request.GET.get('cod', '')
    values = retrieveValues(cod)
    path = os.path.join(os.path.dirname(__file__), 'templates/base_pac.html')
    html = template.render(path, values)
    return HttpResponse(html) ## or

def retrieveValues(cod):
    data = simplejson.load(open('pac_data.json','rb'))
    for d in data:
        d['valor'] = int(d['valor'])
    
    censo = simplejson.load(open('censo_sp.json','rb'))
    
    investimento = {}
    for d in data:
        i = investimento.get(d['cod_ibge'], 0)
        investimento[d['cod_ibge']] = i + d['valor']
    
    for d in data:
        d['investimento_total_no_municipio'] =  investimento.get(d['cod_ibge'], 0)
        for m in censo:
            if m['cod'] == d['cod_ibge']:
                d['populacao'] = int(m['populacao'])
                break
        try:
            d['reais_por_habitante'] = round( d['investimento_total_no_municipio'] / d['populacao'] ,2)
        except KeyError:
            d['reais_por_habitante'] = 0
        
    stats = {"total" : 0}
    
    sorted_x = sorted(data, key=itemgetter('reais_por_habitante'))
    sorted_x.reverse()
    data = sorted_x
    
    template_values = {
        "obras": data,
        "cod": cod,
        "stats": stats,
    }
    
    return template_values

# vim: set ts=4 sw=4 et:
