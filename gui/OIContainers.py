__author__ = 'martino'
from PyQt4.QtGui import QWidget, QPaintEvent, QPainter, QMouseEvent, QPalette, QColor
from PyQt4.QtCore import Qt, QPoint
from core.Managers import BlockManager


class ContainerWidget(QWidget):
    def __init__(self, container, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Container')
        self.__b_widgets = []
        self.__container = container
        self.__translation = QPoint(0, 0)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        for b in container.blocks:
            w = b.get_widget(self)
            self.__b_widgets.append(w)
        pal = QPalette(self.palette())
        pal.setColor(QPalette.Background, QColor(55, 50, 47))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        container.block_added.connect(self.add_block)
        container.block_removed.connect(self.remove_block)
        self.__moving = False
        self.__origin = QPoint()

    def paintEvent(self, e: QPaintEvent):
        if e.isAccepted() and e.accept():
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

    def mousePressEvent(self, e: QMouseEvent):
        BlockManager.deselect_all()
        if e.button() == Qt.LeftButton:
            self.__moving = True
            self.__origin = e.pos()
            self.setCursor(Qt.DragMoveCursor)
        elif e.button() == Qt.RightButton:
            self.show_popup(e.pos())

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        BlockManager.deselect_all()
        if e.button() == Qt.LeftButton:
            self.__moving = False
            self.__translation = QPoint()
            self.translate(0, 0)

    def show_popup(self, pos):
        print('here')

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.__moving:
            dx = e.x() - self.__origin.x()
            dy = e.y() - self.__origin.y()
            self.__origin = e.pos()
            self.translate(dx, dy)

    def mouseReleaseEvent(self, e):
        self.__moving = False
        self.setCursor(Qt.ArrowCursor)

    def translate(self, dx, dy):
        p = QPoint(self.__translation.x() + dx, self.__translation.y() + dy)
        self.__translation = p
        for b in self.__b_widgets:
            b.translate(p)
        self.repaint()
