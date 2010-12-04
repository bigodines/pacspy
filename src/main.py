import csv
import re
import simplejson as json

def format_value(old_val):
	tmp = re.findall('\d+', old_val)
	new_val = ''.join(tmp[:-1])
	return new_val


# reader = csv.reader(open('resources/PAC_SP_por_cidade.csv','rb'))
# writer = csv.writer(open('resources/PAC_com_valor_normalizado.csv', 'wb'))

# keys = ["area", "municipio", "proponente", "tipo", "data", "valor", "estagio"]
# pac_data = []
# for line in reader:
# 	data = {}
# 	line[5] = format_value(line[5])
# 	out = dict(zip(keys, line))
# 	pac_data.append(out)


reader = csv.reader(open('resources/censo2010_SP.csv','rb'))
keys = ["cod","mesorregiao", "nome_mesorregiao", "microrregiao", "nome_microrregiao", "cidade", "uf", "1970", "1980", "1981", "2000", "2007", "populacao", "homens", "mulheres", "urbana", "rural", "crescimento"]
censo_data = []
for line in reader:
	censo_data.append(dict(zip(keys,line)))
	
print json.dumps(censo_data, indent=4)
