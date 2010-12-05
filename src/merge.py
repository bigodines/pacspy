#!/usr/bin/env python
# encoding: utf-8
import csv
import re
import simplejson as json
from unicodedata import normalize

# DEPENDENCE: install python-yql from http://python-yql.org/ or with sudo pip install yql
import yql

def remove_acentos(txt):
	# deixa no padrao para a tabela brazil.ibge.search do YQL
	return txt.replace( u'Á','A' ).replace( u'É','E' ).replace( u'Í','I' ).replace( u'Ó','O' ).replace( u'Ú','U' ).replace( u'Ã','A' ).replace( u'Õ','O' ).replace( u'Â','A' ).replace( u'Ê','E' ).replace( u'Ô','O' ).replace( u"'","`" ).replace( u"Ç","C" )

class Merge(object):
	def __init__(self):
		self.pac = json.load(open('../resources/pac_latest.json','rb'))
		self.censo = json.load(open('../resources/censo_sp.json','rb'))
		self.prefeitos = json.load(open('../resources/prefeitos_sp.json','rb'))
	
	def first_merge(self):
		self.pac = json.load(open('../resources/normalizado.json','rb'))
		municipios = {}
		for muni in censo:
			municipios[muni['cidade']] = muni['cod']	
		for obra in pac:
			obra['cod_ibge'] = municipios.get(obra['municipio'])
	
	def valor_to_int(self):
		self.pac = json.load(open('../resources/pac_com_cod_ibge.json','rb'))
		for p in self.pac:
			p['valor'] = int(p['valor'])
			
	def add_populacao(self):		
		for d in self.pac:
			for m in self.censo:
				if m['cod'] == d['cod_ibge']:
					d['populacao'] = int(m['populacao'])
					break
					
	def add_reais_por_habitante(self):
		investimento = {}
		for d in self.pac:
			i = investimento.get(d['cod_ibge'], 0)
			investimento[d['cod_ibge']] = i + d['valor']
		
		for d in self.pac:
			d['investimento_total_no_municipio'] =  investimento.get(d['cod_ibge'], 0)
			try:
				d['reais_por_habitante'] = round( d['investimento_total_no_municipio'] / d['populacao'] ,2)
			except KeyError:
				d['reais_por_habitante'] = 0
	
	def normalize_prefeitos(self):
		
		y = yql.Public()
		env = "http://datatables.org/alltables.env"
		query = "select * from brazil.ibge.search where query=@municipio and state='SP'"
		for p in self.prefeitos[:2]:
			
			r = y.execute(query, env=env, params={"municipio": remove_acentos(p['municipio'])})
			
			print r
			city = r.results['city']
			print remove_acentos(p['municipio']), " >>> " ,city['name'], " >>> ", city['ibge_code']
			
				
	def dump(self, myjson):
		print json.dumps(myjson, indent=4)

def main():
	m = Merge()
	m.normalize_prefeitos()
	#m.dump(m.pac)
	

if __name__ == '__main__':
	main()

