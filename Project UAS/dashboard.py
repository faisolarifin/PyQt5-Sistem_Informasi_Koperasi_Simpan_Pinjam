from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow

class Dashboard(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        loadUi('./ui/dashboard.ui', self)
        self.setWindowTitle('Dashboard')
        self.Animasi()

    def Animasi(self):
        self.anim = QPropertyAnimation(self.label, b"geometry")
        self.anim.setDuration(8000)
        self.anim.setStartValue(QRect(230, -100, 945, 215))
        self.anim.setEndValue(QRect(230, 180, 945, 215))
        self.anim.start()