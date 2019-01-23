import threading
import time

import mvg_api
import wx

name = "mvg"

class GridFrame(wx.Frame):
    X_POS = 3800
    Y_POS = 0
    STATION = "Richard-Strauss-Straße"
    STATIONID = mvg_api.get_id_for_station(STATION)
    ALLOWED_LABLES = ["U4"]
    FORBIDDEN_LABELS = []

    def __init__(self):

        # GUI Implementation
        wx.Frame.__init__(self, parent=None, title=self.STATION, size=(315, 450))

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.SetPosition((self.X_POS, self.Y_POS))

        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0

        self.list_ctrl = wx.ListCtrl(panel, size=(-1, 500),
                                     style=wx.LC_REPORT
                                           |wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, 'Linie', width=40)
        self.list_ctrl.InsertColumn(1, 'Ziel', width=180)
        self.list_ctrl.InsertColumn(2, 'min', width=50)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        # Start of Logic

        self.depatures = mvg_api.get_departures(self.STATIONID)
        self.deltas = []
        self.filterdepatures()

        # Thread is reloading the depatures
        destloader = threading.Thread(target=self.destinationreload)
        destloader.daemon = True
        destloader.start()

        # Thread who is counting down the time
        timecounter = threading.Thread(target=self.timecounter)
        timecounter.daemon = True
        timecounter.start()

    def destinationreload(self):

        def hexToWxColour(h):
            h = h.lstrip('#')
            rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            return wx.Colour(rgb[0], rgb[1], rgb[2], 255)

        def asigndepatures():
            self.list_ctrl.DeleteAllItems()
            self.deltas.clear()
            t = time.time()
            for i, depature in enumerate(self.depatures):
                self.list_ctrl.InsertItem(i, self.depatures[i]['label'])
                self.list_ctrl.SetItem(i, 1, self.depatures[i]['destination'])
                self.list_ctrl.SetItemColumnImage(i, 0, 0)
                self.list_ctrl.SetItemBackgroundColour(i, hexToWxColour(self.depatures[i]['lineBackgroundColor']))
                self.deltas.append(int(self.depatures[i]['departureTime'] / 1000 - t))

        asigndepatures()
        while True:
            if len(self.depatures) > 0:
                sleeptime = (self.depatures[0]['departureTime'] / 1000) - time.time()
                if sleeptime > 0:
                    time.sleep(sleeptime)
                else:
                    time.sleep(10)
                    ndepatures = mvg_api.get_departures(self.STATIONID)
                    if ndepatures[0] != self.depatures[0]:
                        self.depatures = ndepatures
                        self.filterdepatures()
                        asigndepatures()
            else:
                time.sleep(300)

    def timecounter(self):
        while True:
            for i, d in enumerate(self.deltas):
                mins, secs = divmod(self.deltas[i], 60)
                t = '{:02d}:{:02d}'.format(mins, secs)
                self.list_ctrl.SetItem(i, 2, t)
                self.deltas[i] -= 1
            time.sleep(1)

    def filterdepatures(self):
        running = True
        while running:
            running = True
            for i, d in enumerate(self.depatures):
                if len(self.depatures) == 1:
                    i = 0
                    d = self.depatures[i]
                    running = False
                if d['label'] not in self.ALLOWED_LABLES or d['label'] in self.FORBIDDEN_LABELS:
                    del self.depatures[i]
                    break
                if d['departureTimeMinutes'] > 30:
                    del self.depatures[i]
                    break
                running = False
                break

def main():
    app = wx.App(False)
    frame = GridFrame()
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
