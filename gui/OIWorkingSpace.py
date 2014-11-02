__author__ = 'martino'

from PyQt4.QtGui import QWidget, QGridLayout, QPalette, QColor, QResizeEvent


class OIDynBlock:
    def __init__(self, width: float, height: float, parent):
        self.width = width
        self.height = height
        self.parent = parent
        self.h_child = None
        self.v_child = None


class OIWorkingSpace(QWidget):
    def __int__(self, parent=None):
        QWidget.__init__(self, parent)
        # TODO Add intelligent and dynamic layout

    def add_ws_widget(self, w, row, col):
        # TODO do something
        return

    def resizeEvent(self, e: QResizeEvent):
        QWidget.resizeEvent(self, e)


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

