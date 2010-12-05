#!/usr/bin/env python
# encoding: utf-8
import csv
import re
import simplejson as json

class Merge(object):
	def __init__(self):
		self.pac = json.load(open('../resources/pac_latest.json','rb'))
		self.censo = json.load(open('../resources/censo_sp.json','rb'))
	
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
	
	def dump(self, myjson):
		print json.dumps(myjson, indent=4)

def main():
	m = Merge()
	m.add_reais_por_habitante()
	m.dump(m.pac)
	

if __name__ == '__main__':
	main()

