__author__ = 'martino'

from PyQt4.QtGui import QWidget, QGridLayout, QPainter, QPaintEvent, QColor, QPen, QMouseEvent, QComboBox
from PyQt4.QtCore import Qt
from gui.Containers import EditorContainer


class OIMainToolbar(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setMaximumHeight(35)
        self.setMinimumHeight(35)
        self.__layout = QGridLayout(self)
        self.__mode_box = None
        self.init_gui()

    def init_gui(self):
        self.__layout.setMargin(0)

        self.__mode_box = QComboBox(self)
        self.__mode_box.addItem('Logic')
        self.__mode_box.addItem('GUI')
        # self.__mode_box.setMaximumWidth(100)

        self.__layout.addWidget(self.__mode_box, 0, 0)


class OIRightShelf(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setFixedWidth(250)
        self.setMouseTracking(True)
        self.__drag = False

    def paintEvent(self, e: QPaintEvent):
        if not e.isAccepted():
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QColor(0, 0, 0, 0))
        p.setBrush(QColor(55, 50, 47))
        p.drawRect(0, 0, 11, self.height())

        if self.__drag:
            p.setBrush(QColor(255, 255, 255, 180))
        else:
            p.setBrush(QColor(0, 0, 0, 180))
        p.setPen(QPen(QColor(255, 255, 255), 0.5))
        p.drawRoundedRect(1, 10, 20, 20, 2, 2)
        p.setBrush(QColor(205, 205, 205, 180))
        p.drawEllipse(4, 18, 4, 4)

        p.setBrush(self.palette().color(self.backgroundRole()))
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(10, 0, self.width() - 10, self.height())
        p.setPen(QColor(0, 0, 0))
        p.drawLine(10, 0, 10, self.height())

    def mousePressEvent(self, e: QMouseEvent):
        if e.x() <= 12 and 9 <= e.y() <= 31 and e.button() == Qt.LeftButton:
            self.__drag = True
            self.repaint()
        else:
            self.__drag = False

    def mouseReleaseEvent(self, e):
        self.__drag = False
        self.repaint()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.__drag:
            w = self.width() - e.x()
            if w <= 11:
                w = 11
            if w >= 450:
                w = 450
            self.setFixedWidth(w)
        elif e.x() <= 12 and 9 <= e.y() <= 31:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

            # self.setMinimumWidth(e.x())


class OIMainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('OpenIris')
        self.setMinimumSize(600, 400)
        self.__layout = QGridLayout(self)
        self.__layout.setMargin(0)
        self.__layout.setSpacing(0)
        self.__editor = EditorContainer(self)
        self.__toolbar = OIMainToolbar(self)
        self.__right_shelf = OIRightShelf(self)
        self.__layout.addWidget(self.__toolbar, 0, 0, 1, 2)
        self.__layout.addWidget(self.__editor, 1, 0)
        self.__layout.addWidget(self.__right_shelf, 1, 1)
        self.setLayout(self.__layout)

    def editor(self):
        return self.__editor