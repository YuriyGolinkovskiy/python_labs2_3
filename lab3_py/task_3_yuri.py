import wx
import os
import re
import datetime
import logging

#Создайте графическую оболочку для скрипта, написанного в ходе
#выполнения задания № 4 лабораторной работы № 2, в виде диалогового
#окна. Рекомендуется использовать wxPython или PyQt.
class Window(wx.Frame):
    def check_log(self):
        log_filename = "script3.log"
        path = os.path.join(os.getcwd(), log_filename)
        if os.path.exists(path) == False:
            dlg = wx.MessageDialog(
                self, "Файл лога не найден. Файл будет создан автоматически", "Проверка лога", wx.OK)  # создаём всплывашку
            dlg.ShowModal()  # показываем окошко
            logging.basicConfig(filename=log_filename, level=logging.INFO)

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 400))
        # создаём текстовое поле
        self.control = wx.ListBox(self, style=wx.LB_SINGLE)
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-6, -4])
        self.Show(True)
        self.check_log()
        menu_file = wx.Menu()  # создаём экземпляр меню
        # добавляем подпункты к меню
        openItem = menu_file.Append(wx.ID_OPEN, "Открыть", "Откройте файл")
        menu_log = wx.Menu()
        exportItem = menu_log.Append(wx.ID_SAVE, "Экспорт", "Экспорт файла")
        addItem = menu_log.Append(
            wx.ID_ADD, "Добавить в лог", "Обновление лог файла")
        viewItem = menu_log.Append(
            wx.ID_ABOUT, "Просмотр", "Просмотреть лог файл")
        bar = wx.MenuBar()  # создаём рабочую область для меню
        bar.Append(menu_file, "Файл")  # добавляем пункт меню
        bar.Append(menu_log, "Лог")
        # указываем, что это меню надо показать в нашей форме
        self.SetMenuBar(bar)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnExport, exportItem)
        self.Bind(wx.EVT_MENU, self.AddLog, addItem)
        self.Bind(wx.EVT_MENU, self.View, viewItem)

    def OnOpen(self, e):
        self.dirname = " "
        openDlg = wx.FileDialog(self, "Выберите файл для открытия",
                                self.dirname, " ", "*.*")  # создаём диалог
        if openDlg.ShowModal() == wx.ID_OK:  # при выборе файла
            self.filename = openDlg.GetFilename()  # ловим название файла
            self.dirname = openDlg.GetDirectory()  # и папку, в которой он находится
            # открываем файл
            path = os.path.join(self.dirname, self.filename)
            masks = ["\(\d{3}\)\d{7}", "\(\d{3}\)\d{3}-\d{2}-\d{2}"]
            with open(path) as file:
                date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                self.control.Append("Файл " + path +
                                    " был обработан " + date + ":")
                self.control.Append("")
                for i, line in enumerate(file):
                    for mask in masks:
                        for match in re.finditer(mask, line):
                            self.control.Append("Строка " + str(i+1) + ", позиция " + str(match.start()+1) +
                                                " : найдено '{}'".format(line[match.start():match.end()]))
            self.control.Append("")
            self.statusbar.SetStatusText("Обработан файл " + path)
            size = str(os.path.getsize(path))
            size = [''.join(size[::-1][i:i+3])[::-1]
                    for i in range(0, len(size), 3)]
            size = ' '.join(size[::-1])
            self.statusbar.SetStatusText(size + " байт", 1)

    def AddLog(self, e):
        path = os.path.join(os.getcwd(), "script3.log")
        with open(path, "a") as file:
            for line in self.control.GetStrings():
                file.write(line + "\n")

    def OnExport(self, e):
        self.dirname = " "
        openDlg = wx.FileDialog(self, "Выберите файл для записи",
                                self.dirname, " ", "*.*")  # создаём диалог
        if openDlg.ShowModal() == wx.ID_OK:  # при выборе файла
            self.filename = openDlg.GetFilename()  # ловим название файла
            self.dirname = openDlg.GetDirectory()  # и папку, в которой он находится
            # открываем файл
            path = os.path.join(self.dirname, self.filename)
            with open(path, "w") as file:
                for line in self.control.GetStrings():
                    file.write(line + "\n")

    def View(self, e):
        dlg = wx.MessageDialog(
            self, "Вы действительно хотите открыть лог? Данные последних поисков будут потеряны!", "Просмотр лога", wx.YES_NO)  # создаём всплывашку
        if dlg.ShowModal() == wx.ID_YES:
            self.control.Clear()
            path = os.path.join(os.getcwd(), "script3.log")
            with open(path, "r") as file:
                self.control.AppendItems(file.readlines())
            self.statusbar.SetStatusText("Открыт лог")
            self.statusbar.SetStatusText("", 1)
        else:
            dlg.Destroy()


if __name__ == "__main__":
    app = wx.App()
    wnd = Window(None, "Искатель строк")
    app.MainLoop()
