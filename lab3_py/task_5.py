import wx

#Напишите скрипт с графическим интерфейсом пользователя для
#демонстрации работы класса StringFormatter. Разные комбинации
#отмеченных чекбоксов приводят к разным цепочкам операций
#форматирования задаваемой в верхнем поле строки с разными
#результатами
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


class Window(wx.Frame):

    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height))
        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "Строка:", pos=(10, 21), size=(70, 15))
        self.strCtrl = wx.TextCtrl(
            panel, -1, "", pos=(80, 20), size=(width - 110, 20))
        self.checkDel = wx.CheckBox(
            panel, -1, "Удалить слова размером меньше", (80, 60), (220, 20))
        self.sc = wx.SpinCtrl(panel, -1, "", (300, 60), (80, 20))
        wx.StaticText(panel, -1, "букв", pos=(310 +
                                              self.sc.GetSize().width, 62), size=(70, 15))
        self.sc.SetRange(1, 100)
        self.sc.SetValue(5)
        self.checkReplace = wx.CheckBox(
            panel, -1, "Заменить все цифры на *", (80, 90), (220, 20))
        self.cehckInsert = wx.CheckBox(
            panel, -1, "Вставить по пробелу между символами", (80, 120), (250, 20))
        self.checkSort = wx.CheckBox(
            panel, -1, "Сортировать слова в строке", (80, 150), (220, 20))
        self.Bind(wx.EVT_CHECKBOX, self.onRadio, self.checkSort)

        Button = wx.Button(panel, -1, "Форматировать",
                           (80, 270), (width - 110, 40))
        self.radio1 = wx.RadioButton(panel, -1, "По размеру", pos=(100, 180))
        self.radio2 = wx.RadioButton(
            panel, -1, "Лексикографически", pos=(100, 210))
        self.radio1.Enable(False)
        self.radio2.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.format, Button)
        wx.StaticText(panel, -1, "Результат:",
                      pos=(10, height - 80), size=(70, 15))
        self.resCtrl = wx.TextCtrl(
            panel, -1, "", pos=(80, height - 80), size=(width - 110, 20))
        self.Show(True)

    def onRadio(self, event):
        if event.GetEventObject().Value:
            self.radio1.Enable(True)
            self.radio2.Enable(True)
        else:
            self.radio1.Enable(False)
            self.radio2.Enable(False)

    def format(self, event):
        string = StringFormatter(self.strCtrl.Value)
        if self.checkDel.Value:
            string.delete(self.sc.Value)
        if self.checkReplace.Value:
            string.replace()
        if self.checkSort.Value:
            if self.radio1.Value:
                string.sortByLenght()
            elif self.radio2.Value:
                string.sortByLexical()
            else:
                string.sortByLenght()
                self.radio1.SetValue(True)
        if self.cehckInsert.Value:
            string.insertEnter()
        self.resCtrl.SetValue(string.string)


if __name__ == "__main__":
    app = wx.App()
    wnd = Window(None, "StringFormatter", 600, 400)
    app.MainLoop()
