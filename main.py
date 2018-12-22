# -*- coding: utf-8 -*-
import re

table = {'intencje': {'(^[PWŚCS].*)': {'left': '<span style="font-weight: bold"><hr style="width: 100%; height: 2px; margin-top: 50px">',
        'right':'<hr style="width: 100%; height: 2px;"></span>'}, '(^N.*)': {'left': '<span style="font-weight: bold'
        '; color: red"><hr style="width: 100%; height: 2px; margin-top: 50px">',
        'right':'<hr style="width: 100%; height: 2px;"></span>'},
         '(^\d+.\d+)': {'left': '<br><br><span style="font-weight: bold">', 'right': '</span><br>'}},
         'ogloszenia': {'(^\d+\.\D)': {'left': '<br><br>', 'right': ''}}}

split_file_array = {'ogloszenia': ('^\s*1\.\s*', '^\s*INTENCJE\s*'), 'intencje': ('^\s*Poniedziałek\s*', 'OGŁOSZENIA\s*')}
code = {'intencje': '<head><meta charset="UTF-8"></head><body><div style="text-align: center; '
        'font-weight: normal; font-family: Cambria;">', 'ogloszenia': '<head><meta charset="UTF-8">'
        '</head><body><div style="text-align: left; font-weight: normal; font-family: Cambria;">'}

def run():
    return read_file()

def read_file():
    file_to_read = open('OGŁOSZENIA I INTENCJE NA STRONĘ WWW.txt', 'r')
    s = file_to_read.read()
    file_to_read.close()
    return split_file(s)

def split_file(s):
    for pattern in split_file_array:
        index_begin = re.search(split_file_array[pattern][0], s, re.M).start()
        index_end = re.search(split_file_array[pattern][1], s, re.M).start()
        if index_begin > index_end: index_end = len(s)
        part = s[index_begin: index_end]
        split_file_array[pattern] = part
    return format_parts(split_file_array)

def format_parts(split_file_array):
    for s in split_file_array:
        string = split_file_array[s]
        for pattern in table[s]:
            left, right = (table[s][pattern]['left']), (table[s][pattern]['right'])
            string = re.sub(pattern, left + r'\1' + right, string, flags=re.M)
            split_file_array[s] = string
    return create_files(split_file_array)

def create_files(split_file_array):
    for name, string in split_file_array.items():
        file_to_write = open(name+'.html', 'w')
        file_to_write.write(code[name])
        file_to_write.write(string)
        file_to_write.write('</body>')
        file_to_write.close()

if __name__ == "__main__":
    run()
