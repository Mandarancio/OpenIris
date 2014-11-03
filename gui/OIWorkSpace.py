__author__ = 'martino'

from PyQt4.QtGui import QWidget, QGridLayout, QPalette, QColor, QResizeEvent, QMenu, QPainter, QPaintEvent, \
    QMouseEvent, QPushButton, QIcon, QToolBar, QAction
from PyQt4.QtCore import Qt, QPoint, SIGNAL

from core.Utils import Action, Alignment, Info, ViewMode
from gui.Css_Ui import Window_Button, Menu_Button
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
        self.setAutoFillBackground(True)
        self.__objects = []
        self.init()
        self.__type = None
        self.__mode = ViewMode

    def mode(self):
        return self.__mode

    def init(self):
        menu = QMenu('', self)
        menu.menuAction().setIcon(QIcon('rsc/scene.png'))
        a = QAction('Scene', self)
        a.setIconVisibleInMenu(True)
        a.setIcon(QIcon('rsc/scene.png'))
        menu.addAction(a)
        a = QAction('Node', self)
        a.setIcon(QIcon('rsc/node.png'))
        a.setIconVisibleInMenu(True)
        menu.addAction(a)
        a = QAction('Tree', self)
        a.setIcon(QIcon('rsc/tree.png'))
        a.setIconVisibleInMenu(True)
        menu.addAction(a)
        self.addAction(menu.menuAction())
        return


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

    def get_cursor(self, p: QPaintEvent):
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


class OIWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        pal = QPalette(self.palette())
        pal.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(pal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('OpenIris')
        self.setGeometry(.1 * Info.dpi, .1 * Info.dpi, 8 * Info.dpi, 6 * Info.dpi)
        self.setMinimumSize(3 * Info.dpi, 3.3 * Info.dpi)
        self.workspace = OIWorkSpace(self)
        self.workspace.setGeometry(0, .25 * Info.dpi, self.width(), self.height() - 0.30 * Info.dpi)
        self.__origin = QPoint()
        self.__action = Action.NONE
        self.__resize_action = None
        self.setMouseTracking(True)
        self.__close = QPushButton(QIcon('rsc/window-close.png'), '', self)
        self.init_gui()

    def init_gui(self):
        self.__close.setGeometry(self.width() - .23 * Info.dpi, .03 * Info.dpi, .21 * Info.dpi, .2 * Info.dpi)
        self.__close.setStyleSheet(Window_Button)
        self.connect(self.__close, SIGNAL("clicked()"), self.close_window)
        menu = QPushButton('OpenIris', self)
        menu.setGeometry(.02 * Info.dpi, .02 * Info.dpi, .7 * Info.dpi, .22 * Info.dpi)
        menu.setStyleSheet(Menu_Button)

    def close_window(self):
        print('closing')
        self.close()

    def paintEvent(self, e: QPaintEvent):
        if not e.isAccepted():
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QColor(255, 255, 255, 180))
        p.setBrush(QColor(255, 255, 255, 180))
        p.drawRoundedRect(0, 0, self.width(), .5 * Info.dpi, .05 * Info.dpi, .05 * Info.dpi)
        p.drawRect(0, .25 * Info.dpi, self.width(), self.height() - .25 * Info.dpi)

    def resizeEvent(self, e: QResizeEvent):
        QWidget.resizeEvent(self, e)
        self.workspace.setGeometry(0, .25 * Info.dpi, self.width(), self.height() - .30 * Info.dpi)
        self.__close.setGeometry(self.width() - .23 * Info.dpi, .03 * Info.dpi, .21 * Info.dpi, .20 * Info.dpi)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            pos = self.mouse_on_border(e.pos())
            if pos is not None:
                self.__action = Action.RESIZE
                self.__resize_action = pos
                return
            if e.y() <= .25 * Info.dpi:
                if self.isMaximized():
                    self.setWindowState(Qt.WindowNoState)
                    self.__origin = QPoint(0.3 * Info.dpi, .1 * Info.dpi)
                else:
                    self.__origin = e.pos()
                self.__action = Action.DRAG

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.__action == Action.DRAG:
            self.move(e.globalPos() - self.__origin)
            return
        elif self.__action == Action.RESIZE:
            w = self.width()
            h = self.height()
            x = self.x()
            y = self.y()
            dw = e.x()
            dh = e.y()
            if self.__resize_action is Alignment.Right or self.__resize_action is Alignment.BottomRight \
                    or self.__resize_action is Alignment.TopRight:
                if dw >= self.minimumWidth():
                    w = dw
                else:
                    w = self.minimumWidth()
                self.setGeometry(x, y, w, h)
            if self.__resize_action is Alignment.Bottom or self.__resize_action is Alignment.BottomLeft \
                    or self.__resize_action is Alignment.BottomRight:
                if dh >= self.minimumHeight():
                    h = dh
                else:
                    h = self.minimumHeight()
                self.setGeometry(x, y, w, h)
            if self.__resize_action is Alignment.Top or self.__resize_action is Alignment.TopLeft \
                    or self.__resize_action is Alignment.TopRight:
                y = e.globalPos().y()
                x = self.x()
                h -= round(e.y() / 2)
                if h <= self.minimumHeight():
                    return
                self.move(x, y)
                self.setGeometry(x, y, w, h)
            if self.__resize_action is Alignment.Left or self.__resize_action is Alignment.TopLeft \
                    or self.__resize_action is Alignment.BottomLeft:
                x = e.globalX()
                y = self.y()
                w -= round(e.x() / 2)
                if w <= self.minimumWidth():
                    return
                self.move(x, y)
                self.setGeometry(x, y, w, h)
            return

        pos = self.mouse_on_border(e.pos())
        self.setCursor(OIWindow.get_cursor(pos))

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.__action = Action.NONE

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            if not self.isMaximized():
                self.setWindowState(Qt.WindowMaximized)
            else:
                self.setWindowState(Qt.WindowNoState)

    def mouse_on_border(self, pos: QPoint):
        if pos.x() <= 5:
            if pos.y() <= 5:
                return Alignment.TopLeft
            if pos.y() >= self.height() - 5:
                return Alignment.BottomLeft
            return Alignment.Left
        if pos.x() >= self.width() - 5:
            if pos.y() <= 3:
                return Alignment.TopRight
            if pos.y() >= self.height() - 5:
                return Alignment.BottomRight
            return Alignment.Right
        if pos.y() <= 5:
            return Alignment.Top
        if pos.y() >= self.height() - 5:
            return Alignment.Bottom
        return None

    @staticmethod
    def get_cursor(pos: Alignment):
        if pos is None:
            return Qt.ArrowCursor
        if pos is Alignment.Left or pos is Alignment.Right:
            return Qt.SizeHorCursor
        if pos is Alignment.Bottom or pos is Alignment.Top:
            return Qt.SizeVerCursor
        if pos is Alignment.BottomLeft or pos is Alignment.TopRight:
            return Qt.SizeBDiagCursor
        return Qt.SizeFDiagCursor
