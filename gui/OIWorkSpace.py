__author__ = 'martino'

from PyQt4.QtGui import QWidget, QGridLayout, QPalette, QColor, QResizeEvent, QMenu, \
    QMouseEvent, QIcon, QToolBar, QAction
from PyQt4.QtCore import Qt, QPoint, SIGNAL, SLOT, pyqtSlot

from core.Utils import Alignment, Info, ViewMode
from core.Managers import BlockManager
from enum import Enum


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1


class OIDynBlock:
    def __init__(self, width: float, height: float, parent):
        self._width = width
        self._height = height
        self._parent = parent
        self._h_child = None
        self._v_child = None

    def update_size(self, x, y, w, h):
        return


class OIToolBar(QToolBar):
    def __init__(self, parent):
        QToolBar.__init__(self, parent)
        pal = QPalette(self.palette())
        pal.setColor(self.backgroundRole(), QColor(105, 100, 97))
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        self.__objects = []
        self.init()
        self.__type = None
        self.__mode = ViewMode
        self.__menu = None

    def mode(self):
        return self.__mode

    def init(self):
        menu = QMenu('', self)
        menu.menuAction().setIcon(QIcon('rsc/scene.png'))
        a = QAction(QIcon('rsc/scene.png'), 'Scene', self)
        a.setIconVisibleInMenu(True)
        self.connect(a, SIGNAL('triggered()'), self.menu_action)
        menu.addAction(a)
        a = QAction(QIcon('rsc/node.png'), 'Node', self)
        a.setIconVisibleInMenu(True)
        menu.addAction(a)
        self.connect(a, SIGNAL('triggered()'), self.menu_action)
        a = QAction(QIcon('rsc/tree.png'), 'Tree', self)
        a.setIconVisibleInMenu(True)
        menu.addAction(a)
        self.connect(a, SIGNAL('triggered()'), self.menu_action)
        a = QAction(QIcon('rsc/menu.png'), 'Menu', self)
        a.setIconVisibleInMenu(True)
        self.connect(a, SIGNAL('triggered()'), self.menu_action)
        menu.addAction(a)
        self.addAction(menu.menuAction())
        self.__menu = menu
        return

    @pyqtSlot()
    def menu_action(self):
        a = self.sender()
        self.__menu.menuAction().setIcon(a.icon())
        print(a)


class OIWSWidget(QWidget, OIDynBlock):
    def __init__(self, width: float, height: float, parent):
        QWidget.__init__(self, parent)
        OIDynBlock.__init__(self, width, height, parent)
        self.setMinimumSize(0.4 * Info.dpi, 0.4 * Info.dpi)
        self.__layout = QGridLayout(self)
        self.__layout.setSpacing(0)
        self.__layout.setMargin(2)
        self.setLayout(self.__layout)
        self.__toolbar = OIToolBar(self)
        self.__toolbar.setMaximumHeight(0.3 * Info.dpi)
        self.__layout.addWidget(self.__toolbar, 0, 0)
        self.__main_widget = BlockManager.get_viewer(ViewMode.Scene, self)
        pal = QPalette(self.__main_widget.palette())
        pal.setColor(self.backgroundRole(), QColor(55, 50, 47))
        self.__main_widget.setAutoFillBackground(True)
        self.__main_widget.setPalette(pal)
        self.__layout.addWidget(self.__main_widget, 1, 0)
        self.setMouseTracking(True)

    def update_size(self, x, y, w, h):
        ww = round(w * self._width)
        hh = round(h * self._height)
        self.setGeometry(x, y, ww, hh)
        if self._h_child is not None:
            x = self.x() + ww
            y = self.y()
            self._h_child.update_size(x, y, w, h)
        if self._v_child is not None:
            x = self.x()
            y = self.y() + hh
            self._v_child.update_size(x, y, w, h)

    def h_split(self, h: float):
        h_p = self._h_child
        self._width -= h
        w = OIWSWidget(h, 1, self.parent())
        self.setGeometry(self.x(), self.y(), self.width() * (self._width - h), self.height())
        w.setGeometry(self.x() + self.width() * (self._width - h), self.y(), self.width() * h, self.height())
        self._h_child = w
        w._h_child = h_p
        return w

    def v_split(self, v: float):
        v_p = self._v_child
        self._height -= v
        w = OIWSWidget(1, v, self.parent())
        self.setGeometry(self.x(), self.y(), self.width(), self.height() * (self._height - v))
        w.setGeometry(self.x(), self.y() + self.height() * (self._height - v), self.width(), self.height() * v)
        self._v_child = w
        w._v_child = v_p
        return w

    def get_toolbar(self):
        return self.__toolbar

    def mousePressEvent(self, e: QMouseEvent):
        print(self.get_border(e.pos()))

    def mouseMoveEvent(self, e: QMouseEvent):
        self.setCursor(self.get_cursor(e.pos()))

    def get_cursor(self, p: QPoint):
        b = self.get_border(p)
        if b is None:
            return Qt.ArrowCursor
        elif b == Alignment.Left or b == Alignment.Right:
            return Qt.SizeHorCursor
        else:
            return Qt.SizeVerCursor

    def get_border(self, p: QPoint):
        if p.x() <= 2:
            return Alignment.Left
        elif p.x() >= self.width() - 2:
            return Alignment.Right
        elif p.y() <= 2:
            return Alignment.Top
        elif p.y() >= self.height() - 2:
            return Alignment.Bottom
        return None


class OIWorkSpace(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(3 * Info.dpi, 3 * Info.dpi)
        self.setWindowTitle('OpenIris: Workspace')
        pal = QPalette(self.palette())
        pal.setColor(self.backgroundRole(), QColor(105, 100, 97))
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        self.__c_widget = OIWSWidget(1, 1, self)
        self.__c_widget.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, e: QResizeEvent):
        QWidget.resizeEvent(self, e)
        self.__c_widget.update_size(0, 0, self.width(), self.height())

    def central_widget(self):
        return self.__c_widget
