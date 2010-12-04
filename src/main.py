import csv
import re
import simplejson as json

def format_value(old_val):
	tmp = re.findall('\d+', old_val)
	new_val = ''.join(tmp[:-1])
	return new_val


reader = csv.reader(open('resources/PAC_SP_por_cidade.csv','rb'))
writer = csv.writer(open('resources/PAC_com_valor_normalizado.csv', 'wb'))

keys = ["area", "municipio", "proponente", "tipo", "data", "valor", "estagio"]
modified_data = []
for line in reader:
	data = {}
	line[5] = format_value(line[5])
	out = dict(zip(keys, line))
	modified_data.append(out)


	
print json.dumps(modified_data, indent=4)
