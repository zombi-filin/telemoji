# -*- coding: utf-8 -*-
import codecs
import re
import os

#region Обработка списка emoji

# Чтение списка emoji
telemoji_init_path = os.path.join(os.path.dirname(__file__), '..', 'telemoji','__init__.py')
f = open(telemoji_init_path, 'r')
telemoji_init_lines = f.readlines()
f.close()

# Обработка
emoji_list = ''
processed = False

for line in telemoji_init_lines:
    line = line.replace('\n', '')
    if line == '#region emoji list':
        processed = True
    elif line == '#endregion':
        processed = False
    elif processed:
        line = line.replace(' ','')
        line_findall = re.findall(r'(.*?)=\'(.*?)\'', line)
        name = line_findall[0][0]
        unicode_find = line_findall[0][1]
        unicodes = re.findall(r'\\U000([A-Z0-9]{5})', unicode_find)
        unicode_str = ''
        for unicode in unicodes:
            unicode_str = unicode_str + f'&#x{unicode};'
        emoji_list = emoji_list + f'| {name} | {unicode_str} | {unicode_find} |\n'
#endregion

#region Обработка README.MD

# Чтение README.MD
readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
f = codecs.open( readme_path, 'r', 'utf_8' )
readme_lines = f.readlines()
f.close()

# Обработка
readme_str = ''
ignore = False

for line in readme_lines:
    if line.replace('\n', '') == '| :--- | :---: | :--- |':
        readme_str = readme_str + line
        ignore = True
    elif line.replace('\n', '') == '<!-- emoji list end -->':
        ignore = False
        readme_str = readme_str + emoji_list
    if not ignore:
        readme_str = readme_str + line

# Запись README.md
readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
f = codecs.open( readme_path, 'w', 'utf_8' )
f.write(readme_str)
f.close()

#endregion