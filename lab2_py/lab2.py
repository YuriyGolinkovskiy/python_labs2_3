import os
import hashlib
import pathlib
from pathlib import Path
import re
# ------1
# Напишите скрипт, который читает текстовый файл и выводит символы
# в порядке убывания частоты встречаемости в тексте. Регистр символа
# не имеет значения. Программа должна учитывать только буквенные
# символы (символы пунктуации, цифры и служебные символы слудет
# игнорировать). Проверьте работу скрипта на нескольких файлах с
# текстом на английском и русском языках, сравните результаты с
# таблицами, приведенными в wikipedia.org/wiki/Letter_frequencies


def task_1():
    try:
        file_name = input("Введите имя файла(тестовое имя файла task2.txt): ")
        f = open(file_name)
    except IOError as e:
        print("Не удалось открыть файл!!!")
    else:
        file = f.read()
        symbols = {}
        symbols_count = 0
        for symbol in file:
            if symbol.isalpha() and symbols.setdefault(symbol.lower(), 0) >= 0:
                symbols_count += 1
                symbols.update({symbol: symbols.get(symbol)+1})
            list_symbols = list(symbols.items())
            list_symbols.sort(key=lambda i: i[1], reverse=True)
        for i in list_symbols:
            print(i[0]+" : " + str(round(i[1]/symbols_count*100, 3)) + "%")

# -------2
# Напишите скрипт, позволяющий искать в заданной директории и в ее
# подпапках файлы-дубликаты на основе сравнения контрольных сумм
# (MD5). Файлы могут иметь одинаковое содержимое, но отличаться
# именами. Скрипт должен вывести группы имен обнаруженных файловдубликатов.


def task_2():
    folder = input("Введите путь(тестовый путь dir2): ")
    duplicates = {}
    for dirs, subdirs, files in os.walk(folder):
        for name in files:
            file = os.path.join(dirs, name)
            file_hash = hashlib.md5(open(file, 'rb').read()).digest()
            dup = duplicates.get(file_hash)
            if dup:
                try:
                    duplicates[file_hash][name].append(file)
                except KeyError:
                    duplicates[file_hash][name] = [file]
            else:
                duplicates[file_hash] = {name: [file]}
    for item in duplicates:
        for file in duplicates[item]:
            if len(duplicates[item][file]) > 1:
                print('Файлы дубликаты: {}'.format(
                    ', '.join(duplicates[item][file])))

# ----------3
# Задан путь к директории с музыкальными файлами (в названии
# которых нет номеров, а только названия песен) и текстовый файл,
# хранящий полный список песен с номерами и названиями в виде строк
# формата «01. Freefall [6:12]». Напишите скрипт, который корректирует
# имена файлов в директории на основе текста списка песен.


def task_3():
    path_music = Path.cwd() / "dir3"
    mask = "*.mp3"
    conf_file = Path.cwd() / "songs.txt"
    new_name = {}
    try:
        with conf_file.open() as f:
            for line in f:
                s = line.split('[')[0]
                new_name[s.split('.')[1].strip()] = s.strip()
    except IOError:
        print("Не удалось открыть файл!")
    for f in path_music.glob(mask):
        name = f.name.replace(f.suffix, '')
        if len(name.split(".")) == 1:
            f.rename(str(f).replace(name, new_name.get(name)))

# --------------4
# Напишите скрипт, который позволяет ввести с клавиатуры имя
# текстового файла, найти в нем с помощью регулярных выражений все
# подстроки определенного вида, в соответствии с вариантом. Например,
# для варианта № 1 скрипт должен вывести на экран следующее:
# Строка 3, позиция 10 : найдено '11-05-2014'
# Строка 12, позиция 2 : найдено '23-11-2014'
# Строка 12, позиция 17 : найдено '23-11-2014'

# variant5
# найдите все номера телефонов – подстроки вида
# «(000)1112233» или «(000)111-22-33».


def task_4_yuri():
    file_name = "task4_yuri.txt"
    masks = ["\(\d{3}\)\d{7}", "\(\d{3}\)\d{3}-\d{2}-\d{2}"]
    with open(file_name) as file:
        for i, line in enumerate(file):
            for mask in masks:
                for match in re.finditer(mask, line):
                    print("Строка " + str(i+1) + ", позиция " + str(match.start()+1) +
                          " : найдено '{}'".format(line[match.start():match.end()]))

# ----------------5
# Введите с клавиатуры текст. Программно найдите в нем и выведите
# отдельно все слова, которые начинаются с большого латинского
# символа (от A до Z) и заканчиваются 2 или 4 цифрами, например
# «Petr93», «Johnny70», «Service2002». Используйте регулярные
# выражения.


def task_5():
    text = input("Введите текст для поиска: ")
    mask = r"\b[A-Z]\w+\D[0-9]{4}\b|\b[A-Z]\w+\D[0-9]{2}\b"
    res = re.findall(mask, text)
    print(res)


if __name__ == '__main__':
    # task_1()
    # task_2()
    # task_3()
    # task_4_yuri()
    # task_5()
