import csv
import re

def format_value(old_val):
	tmp = re.findall('\d+', old_val)
	new_val = ''.join(tmp[:-1])
	return new_val


reader = csv.reader(open('resources/PAC_SP_por_cidade.csv','rb'))

writer = csv.writer(open('resources/PAC_com_valor_normalizado.csv', 'wb'))

for line in reader:
	line[5] = format_value(line[5])
	writer.writerow(line)
	area = line[0]
	municipio = line[1]
	proponente = line[2]
	desc = line[3]
	data = line[4]
	valor= format_value(line[5])
	status = line[6]

	print line[5], "--->", valor


