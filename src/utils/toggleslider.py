from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class ToggleSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = 0
        self.setOrientation(Qt.Horizontal)
        self.setMinimum(0)
        self.setMaximum(1)
        self.setValue(self.mode)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mode = 1 - self.mode
            self.setValue(self.mode)
        super().mousePressEvent(event)