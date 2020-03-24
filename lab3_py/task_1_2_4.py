from abc import ABC, abstractmethod
import re
import sys
import string


# ------------1
#Задан простой класс Fraction для представления дробей:
#class Fraction(object):
#def __init__(self, num, den):
#self.__num = num
#self.__den = den
#self.reduce()
#def __str__(self):
#return "%d/%d" % (self.__num, self.__den)
#def reduce(self):
#g = Fraction.gcd(self.__num, self.__den)
#self.__num /= g
#self.__den /= g
#@staticmethod
#def gcd(n, m):
#if m == 0:
#return n
#else:
#return Fraction.gcd(m, n % m)
#Дополнить класс таким образом, чтобы выполнялся следующий код:
#frac = Fraction(7, 2)
#print(-frac) # выводит -7/2
#print(~frac) # выводит 2/7
#print(frac**2) # выводит 49/4
#print(float(frac)) # выводит 3.5
#print(int(frac)) # выводит 3

class Fraction(object):
    def __init__(self, num, den):
        self.__num = num
        self.__den = den
        self.reduce()

    def __str__(self):
        return "%d/%d" % (self.__num, self.__den)

    def __neg__(self):
        return "%d/%d" % (-self.__num, self.__den)

    def __invert__(self):
        return "%d/%d" % (self.__den, self.__num)

    def __pow__(self, step):
        return "%d/%d" % (pow(self.__num, step), pow(self.__den, step))

    def __float__(self):
        return self.__num / self.__den

    def __int__(self):
        return round(self.__num // self.__den)

    def reduce(self):
        g = Fraction.gcd(self.__num, self.__den)
        self.__num /= g
        self.__den /= g

    @staticmethod
    def gcd(n, m):
        if m == 0:
            return n
        else:
            return Fraction.gcd(m, n % m)


def task_1():
    frac = Fraction(7, 2)
    print(frac)
    print(-frac)
    print(~frac)
    print(frac**2)
    print(float(frac))
    print(int(frac))


# ------------2
#Напишите классы «Книга» (с обязательными полями: название, автор,
#код), «Библиотека» (с обязательными полями: адрес, номер) и
#корректно свяжите их. Код книги должен назначаться автоматически
#при добавлении книги в библиотеку (используйте для этого
#статический член класса). Если в конструкторе книги указывается в
#параметре пустое название, необходимо сгенерировать исключение
#(например, ValueError). Книга должна реализовывать интерфейс
#Taggable с методом tag(), который создает на основе строки набор тегов
#(разбивает строку на слова и возвращает только те, которые
#начинаются с большой буквы). Например, tag() для книги с названием
#‘War and Peace’ вернет список тегов [‘War’, ‘Peace’]. Реализуйте классы
#таким образом, чтобы корректно выполнялся следующий код:
#lib = Library(1, ’51 Some str., NY’)
#lib += Book(‘Leo Tolstoi’, ‘War and Peace’)
#lib += Book(‘Charles Dickens’, ‘David Copperfield’)
#for book in lib:
# вывод в виде: [1] L.Tolstoi ‘War and Peace’
#print(book)
# вывод в виде: [‘War’, ‘Peace’]
#print(book.tag())

class Toggable(ABC):
    @abstractmethod
    def tag(self):
        pass


class Book(Toggable):
    index = 0

    def tag(self):
        res = []
        for i in self.__name.split():
            if i.istitle():
                res.append(i)
        return res

    def __init__(self, author, name):
        try:
            if name == "":
                raise ValueError("Пустое поле name")
        except ValueError as e:
            print("Exception: ", e)
        else:
            self.__name = name
        finally:
            self.__author = author
            self.__code = Book.indexing()

    def __str__(self):
        # s = "[" + str(self.i) + "] " + \ - другой вариант индексации
        s = "[" + str(self.__code) + "] " + \
            self.__author + " '" + self.__name + "'"
        return s

    @staticmethod
    def indexing():
        Book.index += 1
        return Book.index


class Library():
    def __init__(self, number, address):
        self.__address = address
        self.__number = number
        self.__books = []

    def __iter__(self):
        self.__a = 0
        return self

    def __next__(self):
        if self.__a < len(self.__books):
            x = self.__books[self.__a]
            self.__a += 1
            return x
        else:
            raise StopIteration

    def __iadd__(self, book):
        self.__books.append(book)
        # self.__books[len(self.__books)-1].i = len(self.__books) - другой вариант индексации,если нужно начинать сначала для каждой библиотеки
        return self


def task_2():
    lib = Library(1, '51 Some str., NY')
    lib += Book("Leo Tolstoi", "War and Peace")
    lib += Book("Charlet Dickens", "David Copperfield")
    for book in lib:
        print(book)
        print(book.tag())

# -------------4
#Напишите простой класс StringFormatter для форматирования строк со
#следующим функционалом:
#– удаление всех слов из строки, длина которых меньше n букв;
#– замена всех цифр в строке на знак «*»;
#– вставка по одному пробелу между всеми символами в строке;
#– сортировка слов по размеру;
#– сортировка слов в лексикографическом порядке.

class StringFormatter():
    def __init__(self, str):
        self.__string = str
        self.__separator = " "

    def __str__(self):
        return self.__string

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, value):
        self.__string = value

    @property
    def separator(self):
        return self.__separator

    @separator.setter
    def separator(self, value):
        self.__separator = value

    def delete(self, n):
        words = []
        word = ""
        counter = 0
        lenght = len(self.__string)
        for symbol in self.__string:
            if symbol != self.__separator:
                word += symbol
                counter += 1
            lenght -= 1
            if symbol == self.__separator or lenght == 0:
                if counter >= n:
                    words.append(word)
                word, counter = "", 0
        for w in words:
            word = word + w + self.separator
        self.__string = word[:-1]

    def replace(self):
        new_str = ""
        for symbol in self.__string:
            new_str += "*" if symbol.isdigit() else symbol
        self.__string = new_str

    def insertEnter(self):
        new_str = ""
        for symbol in self.__string:
            new_str += symbol + " "
        self.__string = new_str[:-1]

    def sortByLenght(self):
        words = []
        word = ""
        counter = 0
        lenght = len(self.__string)
        for symbol in self.__string:
            if symbol != self.__separator:
                word += symbol
                counter += 1
            lenght -= 1
            if symbol == self.__separator or lenght == 0:
                words.append([word, counter])
                word, counter = "", 0
        for i in range(len(words)-1):
            for j in range(len(words)-i-1):
                if words[j][1] > words[j+1][1]:
                    words[j], words[j+1] = words[j+1], words[j]
        for i in words:
            word += i[0] + self.__separator
        self.__string = word[:-1]

    def sortByLexical(self):
        words = []
        word = ""
        counter = 0
        lenght = len(self.__string)
        for symbol in self.__string:
            if symbol != self.__separator:
                word += symbol
                counter += 1
            lenght -= 1
            if symbol == self.__separator or lenght == 0:
                words.append(word)
                word, counter = "", 0
        for i in range(len(words)-1):
            for j in range(len(words)-i-1):
                k = 0
                while k != len(words[j]) and k != len(words[j+1]):
                    if ord(words[j][k].lower()) > ord(words[j+1][k].lower()):
                        words[j], words[j+1] = words[j+1], words[j]
                        break
                    elif ord(words[j][k].lower()) < ord(words[j+1][k].lower()):
                        break
                    k += 1
        for i in words:
            word += i + self.__separator
        self.__string = word[:-1]


def task_4():
    st = StringFormatter("Hello guests my GoodBoy Goodnight end")
    st.delete(5)
    st.replace()
    st.sortByLenght()
    st.sortByLexical()
    st.insertEnter()
    print(st)


if __name__ == '__main__':
    # task_1()
    # task_2()
    # task_4()
