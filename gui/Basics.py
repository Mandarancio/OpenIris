__author__ = 'martino'
from core.Settings import Setting
from core.Types import *
from core.UValue import StringValue, BaseValue
from PyQt4.QtGui import QWidget, QPainter, QPaintEvent, QPen, QColor, QMouseEvent, QGraphicsDropShadowEffect, \
    QPainterPath
from PyQt4.Qt import QRectF, QPoint, Qt

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


class Input:
    def __init__(self, t: Type):
        self.type = t


class Output:
    def __init__(self, t: Type):
        self.type = t


class Block(QWidget):
    # TODO add in-output
    border_color = QColor(137, 117, 89)
    border_pen = QPen(border_color, 2)
    selected_pen = QPen(border_color.lighter(), 2)
    padding = 5

    def __init__(self, type_name: str, name: str, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.settings = {"Name": Setting("Name", StringValue("Name", name))}
        self.outputs = {}
        self.inputs = {}
        self.__type_name = type_name
        self._bg_color = QColor(159, 160, 144, 255)
        self._fg_color = QColor(255, 255, 255)
        self._resizable = True
        self.setMinimumSize(90, 120)
        self.__origin = QPoint(0, 0)
        self.__action = Action.NONE
        self.__status = Status.EDIT
        self.__selected = False
        if self._resizable:
            self.__init_corner()

    def __init_corner(self):
        path = QPainterPath()
        path.moveTo(-Block.padding, -15 - Block.padding)
        path.lineTo(-15 - Block.padding, -Block.padding)
        path.lineTo(-Block.padding, -Block.padding)
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
        p.setBrush(self._bg_color)
        p.drawRoundedRect(Block.padding, Block.padding, self.width() - 2 * Block.padding,
                          self.height() - 2 * Block.padding, 8, 8)
        p.setBrush(self._bg_color.darker())
        p.drawRoundedRect(Block.padding, Block.padding, self.width() - 2 * Block.padding, 35 + Block.padding, 8, 8)
        p.setBrush(self._bg_color)
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(1 + Block.padding, 35 + Block.padding, self.width() - 2 - 2 * Block.padding, 10)
        p.setPen(pen)
        p.drawLine(Block.padding, 35 + Block.padding, self.width() - Block.padding, 35 + Block.padding)
        if self._resizable:
            p.setBrush(pen.brush())
            p.drawPath(self.__corner_path.translated(self.width(), self.height()))
        p.setPen(self._fg_color)
        f = p.font()
        f.setPointSize(10)
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRectF(4 + Block.padding, Block.padding + 2, self.width() - 12, 25),
                   str(self.settings["Name"].value()))
        f.setBold(False)
        f.setPointSize(8)
        p.setPen(QColor(self._fg_color.red(), self._fg_color.green(), self._fg_color.blue(), 100))
        p.setFont(f)
        p.drawText(QRectF(4 + Block.padding, 18 + Block.padding, self.width() - 12, 15), str(self.__type_name))
        p.setPen(QPen(pen.brush(), 1))
        self._paint_ins(p)
        self._paint_outs(p)
        self._paint_content(p)

    def _paint_ins(self, p: QPainter):
        y = 40 + Block.padding
        x = 1
        for i in self.inputs:
            p.setBrush(self.inputs[i].type.color())
            p.drawEllipse(x, y, 9, 9)
            y += 13

    def _paint_outs(self, p: QPainter):
        y = 40 + Block.padding
        x = self.width() - 10
        for i in self.outputs:
            p.setBrush(self.outputs[i].type.color())
            p.drawEllipse(x, y, 9, 9)
            y += 13

    def _paint_content(self, p: QPainter):
        # nothing to do
        return

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
        if self._resizable:
            if abs(e.x() - self.width()) < 8 + Block.padding and abs(
                            e.y() - self.height()) < 8 + Block.padding and self._check_action(Action.RESIZE):
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
        if self._resizable:
            width = w if w >= self.minimumWidth() else self.minimumWidth()
            height = h if h >= self.minimumHeight() else self.minimumHeight()
            self.setGeometry(self.x(), self.y(), width, height)


class VariableBlock(Block):
    def __init__(self, name: str="Var", parent=None):
        Block.__init__(self, "Variable", name, parent)
        self._resizable = False
        self._bg_color = QColor(233, 221, 175)
        self._fg_color = QColor(0, 0, 0)
        self.settings["Value"] = BaseValue("Value", NoneType())
        self.inputs["Value"] = Input(NoneType())
        self.outputs["Value"] = Output(NoneType())

    def _paint_content(self, p: QPainter):
        t = self.settings["Value"].type()
        p.setPen(self._fg_color)
        f = self.font()
        f.setPointSize(9)
        p.setFont(f)
        p.drawText(QRectF(Block.padding + 5, self.height() / 2 + 10, self.width() - Block.padding * 2 - 10,
                          30), Qt.AlignCenter, str(t))

        f.setPointSize(12)
        p.setFont(f)
        s = 'None'
        if self.settings["Value"].data() is not None:
            s = str(self.settings["Value"])
        p.drawText(QRectF(Block.padding + 5, self.height() / 2 - 5, self.width() - Block.padding * 2 - 10,
                          30), Qt.AlignCenter, s)