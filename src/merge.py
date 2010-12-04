#!/usr/bin/env python
# encoding: utf-8
import csv
import re
import simplejson as json

def main():
	pac = json.load(open('../resources/normalizado.json','rb'))
	censo = json.load(open('../resources/censo_sp.json','rb'))

	municipios = {}
	
	for muni in censo:
		municipios[muni['cidade']] = muni['cod']
	
	for obra in pac:
		obra['cod_ibge'] = municipios.get(obra['municipio'])
		
	print json.dumps(pac, indent=4)
	

if __name__ == '__main__':
	main()

