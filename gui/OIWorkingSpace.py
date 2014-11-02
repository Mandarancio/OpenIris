__author__ = 'martino'

from PyQt4.QtGui import QWidget, QGridLayout, QPalette, QColor


class OIWorkingSpace(QWidget):
    def __int__(self, parent=None):
        QWidget.__init__(self, parent)


class OIWSWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(40, 40)
        self.__layout = QGridLayout(self)
        self.__layout.setSpacing(0)
        self.__layout.setMargin(1)
        self.setLayout(self.__layout)
        self.__toolbar = QWidget(self)
        self.__toolbar.setMaximumHeight(25)
        self.__layout.addWidget(self.__toolbar, 0, 0)
        self.__main_widget = QWidget(self)
        pal = QPalette(self.__main_widget.palette())
        pal.setColor(self.backgroundRole(), QColor(55, 50, 47))
        self.__main_widget.setAutoFillBackground(True)
        self.__main_widget.setPalette(pal)
        self.__layout.addWidget(self.__main_widget, 1, 0)
