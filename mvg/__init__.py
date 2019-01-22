import threading
import time

import mvg_api
import wx


class GridFrame(wx.Frame):
    def __init__(self):

        self.depatures = mvg_api.get_departures(680)

        wx.Frame.__init__(self, parent=None, title="Abfahrten an der Richard Strauss Straße", size=(310, 400))

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0

        self.list_ctrl = wx.ListCtrl(panel, size=(-1, 500),
                                     style=wx.LC_REPORT
                                           |wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, '', width=40)
        self.list_ctrl.InsertColumn(1, '', width=180)
        self.list_ctrl.InsertColumn(2, '', width=50)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

        t = threading.Thread(target=self.destinationreload)
        t.daemon = True
        t.start()

    def destinationreload(self):

        def hexToWxColour(h):
            h = h.lstrip('#')
            rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            return wx.Colour(rgb[0], rgb[1], rgb[2], 255)

        def asigndepatures(self):
            self.list_ctrl.DeleteAllItems()
            for i, depature in enumerate(self.depatures):
                if self.depatures[i]['departureTimeMinutes'] > 30:
                    break;

                self.list_ctrl.InsertItem(i, self.depatures[i]['label'])
                self.list_ctrl.SetItem(i, 1, self.depatures[i]['destination'])
                self.list_ctrl.SetItem(i, 2, str(self.depatures[i]['departureTimeMinutes']))
                self.list_ctrl.SetItemColumnImage(i, 0, 0)
                self.list_ctrl.SetItemBackgroundColour(i, hexToWxColour(self.depatures[i]['lineBackgroundColor']))

        # def timereloader(self):

        asigndepatures(self)
        while True:
            sleepTime = (self.depatures[0]['departureTime'] / 1000) - time.time()
            print(self.depatures[0]['departureTime'] / 1000)
            print(time.time())
            print(self.depatures[0])
            print(sleepTime)
            if sleepTime > 0:
                time.sleep(sleepTime)
            else:
                time.sleep(15)
                ndepatures = mvg_api.get_departures(680)
                if (ndepatures[0] != self.depatures[0]):
                    self.depatures = ndepatures
                    asigndepatures(self)





if __name__ == '__main__':

    app = wx.App(False)
    frame = GridFrame()  # id 680
    frame.Show(True)
    app.MainLoop()