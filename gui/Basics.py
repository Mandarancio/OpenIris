__author__ = 'martino'
from core.BlockDef import BlockDef
from PyQt4.QtGui import QWidget, QPainter, QPaintEvent, QPen, QColor, QMouseEvent
from PyQt4.Qt import QRectF, QPoint
from enum import Enum


class Action(Enum):
    NONE = 0
    DRAG = 1
    RESIZE = 2
    CONNECTING = 3


class Status(Enum):
    EDIT = 0
    RUN = 1
    DEBUG = 2


class Block(QWidget):
    border_color = QColor(55, 55, 55)
    border_pen = QPen(border_color, 2)

    def __init__(self, b_def: BlockDef, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.__def = b_def
        self.setMinimumSize(90, 120)
        self.__origin = QPoint(0, 0)
        self.__action = Action.NONE
        self.__status = Status.EDIT

    def _paint(self, p: QPainter):
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Block.border_pen)
        p.setBrush(self.__def.bg_color())
        p.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 8, 8)
        p.setBrush(self.__def.bg_color().darker())
        p.drawRoundedRect(2, 2, self.width() - 4, 43, 8, 8)
        p.setBrush(self.__def.bg_color())
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(3, 37, self.width() - 6, 10)
        p.setPen(Block.border_pen)
        p.drawLine(2, 37, self.width() - 2, 37)
        p.setPen(self.__def.fg_color())
        f = p.font()
        f.setPointSize(10)
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRectF(6, 6, self.width() - 12, 25), str(self.__def.settings["Name"].value()))
        f.setBold(False)
        f.setPointSize(8)
        p.setPen(QColor(255, 255, 255, 100))
        p.setFont(f)
        p.drawText(QRectF(6, 22, self.width() - 12, 15), str(self.__def.type_name()))

    def paintEvent(self, e: QPaintEvent):
        if e.isAccepted():
            p = QPainter(self)
            self._paint(p)

    def _check_action(self, action):
        if self.__action != Action.NONE and action != Action.NONE:
            return False
        return True

    def mousePressEvent(self, e: QMouseEvent):
        if self._check_action(Action.DRAG):
            self.__origin = e.pos()
            self.__action = Action.DRAG

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.__action == Action.DRAG:
            dx = e.x() - self.__origin.x()
            dy = e.y() - self.__origin.y()
            self.parent().repaint(self.geometry())
            self.setGeometry(self.x() + dx, self.y() + dy, self.width(), self.height())

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.__action = Action.NONE