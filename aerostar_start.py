import os

print("hello.")
print('''формат входного файла:

код ключа;табельный номер;ФИО

565A2C7983;777701;Сагайдак Олександр

можно получить предварительно подготовив таблицу в EXEL и сохранить в формате .csv''')
print("Выберите файл для импорта. Список файлов в текущем каталоге:")
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    print("[{}] : {}".format(files.index(f), f))

while True:
    try:
        input_file_name = input('Введите имя или номер файла из списка: ')
        if input_file_name in files:
            #  print("file find")
            break
        elif isinstance(int(input_file_name), int):
            #  print('number find')
            input_file_name = files[int(input_file_name)]
            break
    except (ValueError, IndexError):
        print("incorrect file name. try again")
        continue
print("input file: ", input_file_name)

xml_header = '''
<?xml version="1.0" encoding="utf-8"?>
<RK7DataBase version="1" dataSource="" dataVersion="">
	<DATAPACKET Version="2.0" Name="DEVICEDATALOOKUPITEMS" IndexFieldNames="SIFR;">
		<METADATA>
			<FIELDS>
				<FIELD attrname="SIFR" fieldtype="i4"/>
				<FIELD attrname="GUIDSTRING" fieldtype="string" WIDTH="39"/>
				<FIELD attrname="RAWINPUTDATA" fieldtype="string" WIDTH="41"/>
				<FIELD attrname="SUBSTITUDEMODE" fieldtype="i2"/>
				<FIELD attrname="DECODEDDATA" fieldtype="string" WIDTH="41"/>
				<FIELD attrname="OBJREFNO" fieldtype="i2"/>
				<FIELD attrname="OBJIDENT" fieldtype="i4"/>
				<FIELD attrname="FLAGS" fieldtype="i4"/>
				<FIELD attrname="RECSTAMP" fieldtype="string" WIDTH="39"/>
			</FIELDS>
			<PARAMS/>
		</METADATA>
		<ROWDATA>
'''
xml_body = ''
xml_footer = '''
        </ROWDATA>
	</DATAPACKET>
</RK7DataBase>
'''

txt_body = ''
card_expire = '10.10.2030'
i = 0
separator = ";"

txt_report = 'начало отчета\n'


with open(input_file_name) as f:
    for line in f:
        sep_line = line.split(separator)
        sep_line = [lin.rstrip() for lin in sep_line]
        #  print(sep_line)
        rfid_key = sep_line[0]
        rfid_key = '{4}{5};{6}{7}{8}{9}'.format(*rfid_key)
        #  print(rfid_key)
        sep_rfid_key = rfid_key.split(";")
        sep_rfid_key = [key.rstrip() for key in sep_rfid_key]
        #  print(sep_rfid_key)
        raw_1byte_rfid = int(sep_rfid_key[0], 16)
        raw_2byte_rfid = int(sep_rfid_key[1], 16)
        raw_1byte_rfid = str(raw_1byte_rfid)
        raw_2byte_rfid = str(raw_2byte_rfid)
        while len(raw_1byte_rfid) < 3:
            raw_1byte_rfid = '0' + raw_1byte_rfid
        while len(raw_2byte_rfid) < 5:
            raw_2byte_rfid = '0' + raw_2byte_rfid
        raw_input_data = raw_1byte_rfid + raw_2byte_rfid
        decoded_data = sep_line[1]
        sifr = sep_line[1]
        guidstring = sep_line[1]
        while len(guidstring) < 8:
            guidstring = '0' + guidstring
        xml_body += '<ROW SIFR="' + str(sifr) + '" GUIDSTRING="{' + str(guidstring) + '-7F11-1234-BBCD-4A4B4C4D4E4F4}" RAWINPUTDATA="' + raw_input_data + '" SUBSTITUDEMODE="1" DECODEDDATA="' + 'PDS' + str(decoded_data) + '" OBJREFNO="0" OBJIDENT="0" FLAGS="0"/>\n'
        txt_body += '{},{},2,,,{},1\n'.format(decoded_data, card_expire, sep_line[2])
        i += 1
        txt_report += '{:3}: {:10} {:10} {:10} {}\n'.format(i, sep_line[0], sep_line[1], raw_input_data, sep_line[2])
        print('{:3}: {:10} {:10} {:10} {}'.format(i, sep_line[0], sep_line[1], raw_input_data, sep_line[2]))

output_xml_name = os.path.splitext(input_file_name)[0] + '_for_rk7.xml'
with open(output_xml_name, 'w') as d:
    d.write(xml_header + xml_body + xml_footer)
output_txt_name = os.path.splitext(input_file_name)[0] + '_for_pcards.txt'
with open(output_txt_name, 'w') as d:
    d.write(txt_body)
output_txt_name = os.path.splitext(input_file_name)[0] + '_report.txt'
with open(output_txt_name, 'w') as d:
    d.write(txt_report)

print("Фаил {} записан.\nФаил {} записан.\nКоличество строк: {}".format(output_xml_name, output_txt_name, i))
input("Нажми Enter для выхода.")
