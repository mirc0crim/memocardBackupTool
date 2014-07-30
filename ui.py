import memo
import datetime
import time
import wx

class MyFrame(wx.Frame):

    logger = None
    l = ["Memocard 1 -> PC", "Memocard 2 -> PC", "Memocard 1 -> Netz", "Memocard 2 -> Netz", "Memocard <-> Memocard", "Reparieren"]
    
    def __init__(self, t):
        wx.Frame.__init__(self, None, title=t, size=(800,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        panel = wx.Panel(self)

        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        # the combobox Control
        driveList = ['E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:']
        # dev 1
        self.textDrive1 = wx.StaticText(panel, label="Laufwerk Memocard 1")
        grid.Add(self.textDrive1, pos=(1,0))
        self.drive1 = wx.ComboBox(panel, size=(100, -1), choices=driveList, style=wx.CB_DROPDOWN)
        self.drive1.SetValue(driveList[1])
        grid.Add(self.drive1, pos=(1,1))
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.drive1)
        # dev 2
        self.textDrive2 = wx.StaticText(panel, label="Laufwerk Memocard 2")
        grid.Add(self.textDrive2, pos=(2,0))
        self.drive2 = wx.ComboBox(panel, size=(100, -1), choices=driveList, style=wx.CB_DROPDOWN)
        self.drive2.SetValue(driveList[2])
        grid.Add(self.drive2, pos=(2,1))
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox2, self.drive2)

        # Checkbox
        self.doit = wx.CheckBox(panel, label="Richtig kopieren/entfernen?")
        self.doit.SetValue(False)
        grid.Add(self.doit, pos=(4,0), span=(1,2), flag=wx.BOTTOM, border=5)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.doit)

        # 6 Buttons
        self.button1 =wx.Button(panel, size=(150,30), label=MyFrame.l[0])
        self.Bind(wx.EVT_BUTTON, self.OnClick1, self.button1)
        grid.Add(self.button1, pos=(6,0))
        self.button2 =wx.Button(panel, size=(150,30), label=MyFrame.l[1])
        self.Bind(wx.EVT_BUTTON, self.OnClick2, self.button2)
        grid.Add(self.button2, pos=(6,1))

        self.button3 =wx.Button(panel, size=(150,30), label=MyFrame.l[2])
        self.Bind(wx.EVT_BUTTON, self.OnClick3, self.button3)
        grid.Add(self.button3, pos=(7,0))
        self.button4 =wx.Button(panel, size=(150,30), label=MyFrame.l[3])
        self.Bind(wx.EVT_BUTTON, self.OnClick4, self.button4)
        grid.Add(self.button4, pos=(7,1))
        
        self.button5 =wx.Button(panel, size=(150,30), label=MyFrame.l[4])
        self.Bind(wx.EVT_BUTTON, self.OnClick5, self.button5)
        grid.Add(self.button5, pos=(8,0), span=(1,2), flag=wx.EXPAND)
        
        self.button6 =wx.Button(panel, size=(150,30), label=MyFrame.l[5])
        self.Bind(wx.EVT_BUTTON, self.OnClick6, self.button6)
        grid.Add(self.button6, pos=(11,0), span=(1,2), flag=wx.EXPAND)

        # A multiline TextCtrl
        MyFrame.logger = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(MyFrame.logger, 1, wx.EXPAND)
        panel.SetSizerAndFit(hSizer)

    def EvtComboBox(self, event):
        if len(event.GetString()) < 2:
            return
        MyFrame.logger.AppendText("Memocard 1: \n")
        memo.cardPath = event.GetString() + memo.cardPath[2:]
        MyFrame.logger.AppendText(memo.cardPath + "\n")
    def EvtComboBox2(self, event):
        MyFrame.logger.AppendText("Memocard 2: \n")
        memo.card2Path = event.GetString() + memo.card2Path[2:]
        MyFrame.logger.AppendText(memo.card2Path + "\n")
    def OnClick1(self,event):
        self.clicked(memo.mem1ToPc, MyFrame.l[0])
    def OnClick2(self,event):
        self.clicked(memo.mem2ToPc, MyFrame.l[1])
    def OnClick3(self,event):
        self.clicked(memo.mem1ToNet, MyFrame.l[2])
    def OnClick4(self,event):
        self.clicked(memo.mem2ToNet, MyFrame.l[3])
    def OnClick5(self,event):
        self.clicked(memo.memToMem, MyFrame.l[4])
    def OnClick6(self,event):
        self.clicked(memo.tryRepair, MyFrame.l[5])
    def EvtCheckBox(self, event):
        memo.counter = 0
        if memo.doIt:
            memo.doIt = False
            MyFrame.logger.AppendText("\nNur Vorschau\n\n")
        else:
            memo.doIt = True
            MyFrame.logger.AppendText("\nRichtig kopieren und entfernen\n\n")
    def OnClose(self, event):
        loggerValue = MyFrame.logger.GetValue()
        if len(loggerValue) > 1:
            now = datetime.datetime.now()
            dateString = "%d%02d%02d" % (now.year, now.month, now.day)
            dateString += "%02d%02d%02d" % (now.hour, now.minute, now.second)
            f = open("D:\\Memocard Backup Tool\\log\\" + dateString + ".txt", "w+")
            f.write(MyFrame.logger.GetValue())
            f.close()
        self.Destroy()
    def clicked(self, f, s):
        MyFrame.logger.AppendText(s + "\n")
        start = time.time()
        f()
        totalTime = round((time.time() - start)*10)/10
        if memo.doIt:
            MyFrame.logger.AppendText("Fertig in " + str(totalTime) + " Sekunden\n")
            memo.counter = 0
        else:
            if memo.counter <> 0:
                mult = 0
                if s in (MyFrame.l[0], MyFrame.l[1]):
                    mult = 8
                if s in (MyFrame.l[2], MyFrame.l[3]):
                    mult = 12
                if s == MyFrame.l[4]:
                    mult = 16
                MyFrame.logger.AppendText("\nDauert ca. " + str(memo.counter*mult) + "s\n")
                memo.counter = 0
            MyFrame.logger.AppendText("Fertig\n")

def addText(s):
    MyFrame.logger.AppendText(s + "\n")

def create():
    app = wx.App(False)
    top = MyFrame("Memocard Backup Tool")
    favicon = wx.Icon("C:\Python27\DLLs\py.ico", wx.BITMAP_TYPE_ICO, 16, 16)
    top.SetIcon(favicon)
    top.Show()
    app.MainLoop()
