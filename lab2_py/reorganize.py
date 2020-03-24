import os
import sys
import argparse
import datetime
import shutil

# Напишите скрипт reorganize.py, который в директории --source создает
# две директории: Archive и Small. В первую директорию помещаются
# файлы с датой изменения, отличающейся от текущей даты на
# количество дней более параметра --days (т.е. относительно старые
# файлы). Во вторую – все файлы размером меньше параметра --size байт.
# Каждая директория должна создаваться только в случае, если найден
# хотя бы один файл, который должен быть в нее помещен. Пример
# вызова:
# reorganize --source "C:\TestDir" --days 2 --size 4096

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', default=os.getcwd())
    parser.add_argument('-d', '--days', default=2)
    parser.add_argument('-S', '--size', default=4096)

    return parser


def create_directory(name, source):
    path = source + "/" + name
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print("Не удалось создать директорию: " + name)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    date_now = datetime.datetime.now()
    for file in os.listdir(namespace.source):
        if os.path.isfile(os.path.join(namespace.source, file)):
            d = os.path.getmtime(file)
            date_modify = datetime.datetime.fromtimestamp(d)
            size = os.path.getsize(file)
            if (date_now - date_modify).days > int(namespace.days):
                create_directory("Archive", namespace.source)
                shutil.copy(file, os.path.join(namespace.source, "Archive"))
            if size < int(namespace.size):
                create_directory("Small", namespace.source)
                shutil.copy(file, os.path.join(namespace.source, "Small"))
