__author__ = 'martino'
from core.BlockDef import BlockDef
from PyQt4.QtGui import QWidget, QPainter, QPaintEvent, QPen, QColor, QMouseEvent, QGraphicsDropShadowEffect, \
    QPainterPath
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
    border_color = QColor(137, 117, 89)
    border_pen = QPen(border_color, 2)
    selected_pen = QPen(QColor(255, 255, 255), 2)

    def __init__(self, b_def: BlockDef, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.__def = b_def
        self.setMinimumSize(90, 120)
        self.__origin = QPoint(0, 0)
        self.__action = Action.NONE
        self.__status = Status.EDIT
        self.__selected = False
        if self.__def.resizable():
            self.__init_corner()

    def __init_corner(self):
        path = QPainterPath()
        path.moveTo(-2, -17)
        path.lineTo(-17, -2)
        path.lineTo(-2, -2)
        path.closeSubpath()
        self.__corner_path = path


    def selected(self):
        return self.__selected

    def set_selected(self, selected):
        self.__selected = selected

    def deselect(self):
        if self.__selected:
            self.set_selected(False)
            eff = self.graphicsEffect()
            del eff
            self.setGraphicsEffect(None)

    def select(self):
        if not self.__selected:
            self.set_selected(True)
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(20)
            effect.setXOffset(0)
            effect.setYOffset(0)
            effect.setColor(QColor(0, 0, 0, 180))
            self.setGraphicsEffect(effect)
            self.raise_()

    def _paint(self, p: QPainter):
        pen = Block.selected_pen if self.__selected else Block.border_pen
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(pen)
        p.setBrush(self.__def.bg_color())
        p.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 8, 8)
        p.setBrush(self.__def.bg_color().darker())
        p.drawRoundedRect(2, 2, self.width() - 4, 43, 8, 8)
        p.setBrush(self.__def.bg_color())
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(3, 37, self.width() - 6, 10)
        p.setPen(pen)
        p.drawLine(2, 37, self.width() - 2, 37)
        if self.__def.resizable():
            p.setBrush(pen.brush())
            p.drawPath(self.__corner_path.translated(self.width(), self.height()))
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
        self.parent().select(self)
        if self.__def.resizable():
            if abs(e.x() - self.width()) < 10 and abs(e.y() - self.height()) < 10 and self._check_action(Action.RESIZE):
                self.__origin = e.pos()
                self.__action = Action.RESIZE
                return
        if self._check_action(Action.DRAG):
            self.__origin = e.pos()
            self.__action = Action.DRAG

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.__action == Action.DRAG:
            dx = e.x() - self.__origin.x()
            dy = e.y() - self.__origin.y()
            self.set_pos(self.x() + dx, self.y() + dy)
        elif self.__action == Action.RESIZE:
            self.set_size(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.__action = Action.NONE

    def set_pos(self, x: int, y: int):
        xx = x if x >= 0 else 0
        yy = y if y >= 0 else 0
        if xx + self.width() > self.parent().width():
            xx = self.parent().width() - self.width()
        if yy + self.height() > self.parent().height():
            yy = self.parent().height() - self.height()
        self.setGeometry(xx, yy, self.width(), self.height())

    def set_size(self, w: int, h: int):
        if self.__def.resizable():
            width = w if w >= self.minimumWidth() else self.minimumWidth()
            height = h if h >= self.minimumHeight() else self.minimumHeight()
            self.setGeometry(self.x(), self.y(), width, height)

    def settings(self):
        return self.__def.settings