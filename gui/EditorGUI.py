__author__ = 'martino'

from PyQt4.QtGui import QWidget, QGridLayout
from gui.Containers import EditorContainer


class OIMainToolbar(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setMaximumHeight(35)
        self.setMinimumHeight(35)


class OIRightShelf(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setMaximumWidth(250)
        self.setMinimumWidth(100)


class OIMainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('OpenIris')
        self.setMinimumSize(600, 400)
        self.__layout = QGridLayout(self)
        self.__layout.setMargin(0)
        self.__editor = EditorContainer(self)
        self.__toolbar = OIMainToolbar(self)
        self.__right_shelf = OIRightShelf(self)
        self.__layout.addWidget(self.__toolbar, 0, 0, 1, 2)
        self.__layout.addWidget(self.__editor, 1, 0)
        self.__layout.addWidget(self.__right_shelf, 1, 1)
        self.setLayout(self.__layout)

    def editor(self):
        return self.__editor