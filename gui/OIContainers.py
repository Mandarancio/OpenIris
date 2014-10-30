__author__ = 'martino'
from PyQt4.QtGui import QWidget, QPaintEvent, QPainter
from PyQt4.QtCore import Qt

class ContainerWidget(QWidget):
    def __init__(self, container, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.__b_widgets = []
        self.__container = container
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        for b in container.blocks:
            w = b.get_widget(self)
            self.__b_widgets.append(w)

        container.block_added.connect(self.add_block)
        container.block_removed.connect(self.remove_block)

    def paintEvent(self, e: QPaintEvent):
        QWidget.paintEvent(self, e)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for l in self.__container.lines:
            l.paint(p)

    def add_block(self, b):
        w = b.get_widget(self)
        self.__b_widgets.append(w)

    def __get_b_widget(self, b):
        for w in self.__b_widgets:
            if w.block() == b:
                return w
        return None

    def remove_block(self, b):
        w = self.__get_b_widget(b)
        if b is not None:
            self.__b_widgets.remove(b)
            w.deleteLater()