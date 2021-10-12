import zipfile
import os
import hashlib
import requests
import re
import csv

#1 программно разорхивировать в выбранную директорию
directory_to_extract_to = r"C:\\Users\\79277\\PycharmProjects\\pythonProject1\\new_archive"
try:
    os.mkdir(directory_to_extract_to)
except Exception:
    print("Файл уже существует")
else:
    arch_file = zipfile.ZipFile('C:\\Users\\79277\\PycharmProjects\\pythonProject1\\tiff-4.2.0_lab1 (1).zip')
    arch_file.extractall(directory_to_extract_to)
    arch_file.close()
#2.1 Получить список файлов (полный путь) формата sh. Сохранить полученный список
txt_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".txt"):
            txt_files.append(str(root + '\\' + file))
print("Список всех файлов с расширением .txt")
print('\n'.join(txt_files))
# 2.2 Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.
res = []
for file in txt_files:
    data = open(file, 'rb')
    con = data.read()
    res.append(hashlib.md5(con).hexdigest())
    data.close()
print("Хэш:")
print('\n'.join(res))
#3 Найти файл с заданным хэшем
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = r''
target_file_data = ''
for root, dirs, files in os.walk("."):
    for file in files:
        data = os.path.join(root, file)
        file_data = open(data, "rb")
        con = file_data.read()
        if hashlib.md5(con).hexdigest() == target_hash:
            target_file = root + "\\" + file
            target_file_data = con
print("Путь к исходному файлу: ")
print(target_file)
print("Содержимое искомого файла: ")
print(target_file_data)
# 4 Распарсить содержимое страницы
"""
возвращает список всех найденных совпадений re.findall
ищет шаблон в строке и заменяет его на указанную подстроку re.sub
разделяет строку по заданному шаблону re.split
"""
r = requests.get(target_file_data)
result_dct = {} # словарь для записи содержимого таблицы
counter = 0
headers = []
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        # Удаление тегов
        headers = re.sub('\<[^>]*\>', " ", line)
        # Извлечение списка заголовков
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
    else:
        # Удаление тегов
        # Значения в таблице, заключенные в скобках, не учитывать. Для этого удалить скобки и символы между ними.
        # Замена последовательности символов ';' на одиночный символ
        # Удаление символа ';' в начале и в конце строки
        temp = re.sub('<.*?>', ';', line)
        temp = re.sub("\(.*?\)", '', temp)
        temp = re.sub(';+', ';', temp)
        temp = temp[1: len(temp) - 1]
        temp = re.sub('\s(?=\d)', '', temp)
        temp = re.sub('(?<=\d)\s', '', temp)
        temp = re.sub('(?<=0)\*', '', temp)
        temp = re.sub('_', '-1', temp)
 
        tmp_split = temp.split(';')
        if len(tmp_split) == 6:
            tmp_split.pop(0)

        country_name = tmp_split[0]
        country_name = re.sub('.*\s\s', '', country_name)
   
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)
    counter += 1
# 5 Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
w = csv.writer(output, delimiter=";")
w.writerow(headers)
for key, value in result_dct.items():
    w.writerow([key, value[0], value[1], value[2], value[3]])
output.close()
# 6 Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
try:
    print(result_dct[target_country])
except Exception:
    print("Введите корректное значение ")
