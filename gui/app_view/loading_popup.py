from kivy.uix.popup import Popup


class LoadingPopup():
    def __init__(self):
        self.popup = Popup(title="Loading...")
        self.popup.open()

    def close(self):
        if self.popup:
            self.popup.dismiss()