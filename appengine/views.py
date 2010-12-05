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
    return HttpResponse(html)

def PacView(request):
    cod = request.GET.get('cod', '')
    values = retrieveValues(cod)
    path = os.path.join(os.path.dirname(__file__), 'templates/base_pac.html')
    html = template.render(path, values)
    return HttpResponse(html)

def retrieveValues(cod):
    data = simplejson.load(open('pac_data.json','rb'))
    censo = simplejson.load(open('censo_sp.json','rb'))


    stats = {"total" : 0}
    
    sorted_x = sorted(data, key=itemgetter('reais_por_habitante'))
    sorted_x.reverse()
    data = sorted_x
    
    if cod:
        data = [obra for obra in data if obra['cod_ibge']==cod]
        if data:
            stats['nome'] = data[0]['municipio']

            stats['municipio'] = {}
            for m in censo:
                if m['cod'] == cod:
                    stats['municipio'] = m
                    break
                    
    template_values = {
        "obras": data,
        "cod": cod,
        "stats": stats,
    }
    
    return template_values

# vim: set ts=4 sw=4 et:
