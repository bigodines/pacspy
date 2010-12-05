#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from django.utils import simplejson 
from operator import itemgetter


class MainHandler(webapp.RequestHandler):
    def get(self, cod):
	
		data = simplejson.load(open('pac_data.json','rb'))
		
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
		
		if cod:
			data = [obra for obra in data if obra['cod_ibge']==cod]
			if data:
				stats['nome'] = data[0]['municipio']
				
				stats['municipio'] = {}
				for m in censo:
					if m['cod'] == cod:
						stats['municipio'] = m
						break
				if stats['municipio']:
					stats['reais_por_habitante'] = round(stats['total']/ float(stats['municipio']['populacao']),2)
		
		
		template_values = {
			"obras": data,
			"cod": cod,
			"stats": stats,
		}
		
		path = os.path.join(os.path.dirname(__file__), 'templates/base_pac.html')
		self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/pac/?(.*?)', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
