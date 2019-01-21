import mvg_api
import wx


class GridFrame(wx.Frame):
    def __init__(self):

        self.depatures = mvg_api.get_departures(680)

        wx.Frame.__init__(self, parent=None, title="Abfahrten an der Richard Strauss Straße", size=(300, 300))

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0

        self.list_ctrl = wx.ListCtrl(panel, size=(-1,250),
                                     style=wx.LC_REPORT
                                           |wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, '', width=40)
        self.list_ctrl.InsertColumn(1, '', width=180)
        self.list_ctrl.InsertColumn(2, '', width=50)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

        print(self.depatures[1])

    def reload(self):
        self.depatures = mvg_api.get_departures(680)
        for i, depatrue in self.depatures:
            #if self.list_ctrl.FindItem(-1,depatrue['destination']) != -1:
            self.list_ctrl.InsertItem(i, depatrue['destination'])


if __name__ == '__main__':

    app = wx.App(False)
    frame = GridFrame()  # id 680
    frame.Show(True)
    app.MainLoop()