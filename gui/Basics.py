__author__ = 'martino'
import math

from core.Utils import Action, Mode

from PyQt4.QtGui import QWidget, QPainter, QPaintEvent, QPen, QMouseEvent, QGraphicsDropShadowEffect, \
    QPainterPath, QInputDialog, QLineEdit, QRegion
from PyQt4.Qt import QRectF, QPoint, Qt, QObject
import PyQt4.QtCore as QtCore

from core.Settings import Setting
from core.Types import *
from core.UValue import StringValue, BaseValue, IntegerValue
from core.Managers import ValueManager


class Node:
    def __init__(self, t: Type, pos: QPoint, parent):
        self.__type = t
        self.connections = []
        self.lines = []
        self.parent = parent
        self.pos = pos
        self.size = 9

    def type(self):
        return self.__type

    def change_type(self, t: Type):
        self.__type = t
        if len(self.connections) > 0:
            for c in self.connections:
                if not self.compatible(c) or not c.compatible(self):
                    l = self.line_to(c)
                    l.remove()

    def line_to(self, o):
        for l in self.lines:
            if l.connected_to(o):
                return l
        return None

    def abs_pos(self):
        return QPoint(self.pos.x() + self.size / 2 + self.parent.x(), self.pos.y() + self.size / 2 + self.parent.y())

    def disconnect(self, n):
        if n in self.connections:
            self.connections.remove(n)

    def compatible(self, n):
        return self.type().compatible(
            n.type()) and n is not self and self.__class__ is not n.__class__

    def connect(self, n):
        if self.compatible(n):
            self.connections.append(n)

    def paint(self, p: QPainter):
        p.setBrush(self.type().color())
        p.drawEllipse(self.pos.x(), self.pos.y(), self.size, self.size)
        if len(self.lines) > 0:
            pen = p.pen()
            p.setBrush(self.type().color().darker())
            p.setPen(QColor(0, 0, 0, 0))
            p.drawEllipse(self.pos.x() + 2, self.pos.y() + 2, self.size - 4, self.size - 4)
            p.setPen(pen)

    def contains(self, p: QPoint):
        cx = self.pos.x() + self.size / 2.0
        cy = self.pos.y() + self.size / 2.0
        dx = p.x() - cx
        dy = p.y() - cy
        if math.sqrt(dx * dx + dy * dy) <= self.size + 1:
            return True
        return False

    def update(self):
        for l in self.lines:
            l.update()

    def get_line(self):
        return None


class Line:
    def __init__(self, p1: QPoint, p2: QPoint, b1: Node, b2: Node=None):
        self.p1 = p1
        self.p2 = p2
        self.n1 = b1
        self.n2 = b2
        self.selected = False
        self.__path = None
        self._w_parent = None

    def connected_to(self, o: Node):
        if o is self.n1 or o is self.n2:
            return True
        return False

    def remove(self):
        self.n1.lines.remove(self)
        self._w_parent.remove_line(self)
        if self.n2 is not None:
            self.n1.disconnect(self.n2)
            self.n2.disconnect(self.n1)
            self.n2.lines.remove(self)

    def connect(self, n2: Node):
        self.n2 = n2
        self.n1.connect(n2)
        n2.connect(self.n1)
        n2.lines.append(self)
        self.update()

    def disconnect(self, n: Node):
        if self.n1 is n:
            self.n1 = self.n2
            self.n2.disconnect(n)
            n.disconnect(self.n2)
            p = self.p1
            self.p1 = self.p2
            self.p2 = p
            self.n2 = None
        else:
            n.disconnect(self.n1)
            self.n1.disconnect(n)
            self.n2 = None

    def update(self, p2=None):
        if p2 is not None:
            self.p2 = p2
        elif self.n2 is not None:
            self.p2 = self.n2.abs_pos()
        self.p1 = self.n1.abs_pos()
        self.compute_path()
        if self._w_parent is not None:
            self._w_parent.repaint()

    def set_w_parent(self, parent):
        self._w_parent = parent

    def compute_path(self):
        p1 = self.p1 if self.p1.x() < self.p2.x() else self.p2
        p2 = self.p2 if self.p1.x() < self.p2.x() else self.p1
        path = QPainterPath()
        path.moveTo(p1)
        dx = p2.x() - p1.x()
        path.cubicTo(QPoint(p1.x() + dx / 3, p1.y()), QPoint(p2.x() - dx / 3, p2.y()), p2)
        self.__path = path

    def paint(self, p: QPainter):
        if self.__path is None:
            self.compute_path()
        c = Block.border_color
        if self.selected:
            c = c.lighter().lighter()
        p.setPen(QPen(c, 4))
        p.drawPath(self.__path)


class Input(Node):
    value_recive = QtCore.pyqtSignal(BaseValue)

    def __init__(self, t: Type, pos: QPoint, parent):
        Node.__init__(self, t, pos, parent)

    def connect(self, out):
        if self.compatible(out):
            if len(self.connections) >= 1:
                self.lines[0].remove()
            self.connections.append(out)
            return True
        return False

    def get_line(self):
        if len(self.lines) > 0:
            l = self.lines[0]
            self.lines.remove(l)
            l.disconnect(self)
            return l
        p = self.abs_pos()
        l = Line(p, p, self)
        self.lines.append(l)
        return l

    def recive(self, value):
        print(value.data())


class Output(Node):
    signal = QtCore.pyqtSignal(BaseValue)

    def __init__(self, t: Type, pos: QPoint, parent):
        Node.__init__(self, t, pos, parent)

    def connect(self, inp):
        if self.compatible(inp):
            self.connections.append(inp)
            return True
        return False

    def get_line(self):
        p = self.abs_pos()
        l = Line(p, p, self)
        self.lines.append(l)
        return l


class Block(QWidget):
    border_color = QColor(137, 117, 89)
    border_pen = QPen(border_color, 2)
    selected_pen = QPen(border_color.lighter().lighter(), 2)
    padding = 5

    def __init__(self, type_name: str, name: str, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.settings = {"Name": Setting("Name", StringValue(name), parent=self)}
        self.outputs = {}
        self.inputs = {}
        self.__type_name = type_name
        self._bg_color = QColor(159, 160, 144, 255)
        self._fg_color = QColor(255, 255, 255)
        self._resizable = True
        self.setMinimumSize(90, 120)
        self.__origin = QPoint(0, 0)
        self.__action = Action.NONE
        self.__status = Mode.EDIT_LOGIC
        self.__selected = False
        self.__line = None
        if self._resizable:
            self.__init_corner()

    def name(self):
        return self.settings["Name"].data()

    def mode(self):
        return self.__status

    def action(self):
        return self.__action

    def __init_corner(self):
        path = QPainterPath()
        path.moveTo(-Block.padding, -15 - Block.padding)
        path.lineTo(-15 - Block.padding, -Block.padding)
        path.lineTo(-Block.padding, -Block.padding)
        path.closeSubpath()
        self.__corner_path = path

    def _add_input(self, name: str, t: Type):
        if not name in self.inputs:
            x = 1
            y = 40 + Block.padding + len(self.inputs) * 13
            self.inputs[name] = Input(t, QPoint(x, y), self)

    def _add_output(self, name: str, t: Type):
        if not name in self.outputs:
            x = self.width() - 10
            y = 40 + Block.padding + len(self.outputs) * 13
            self.outputs[name] = Output(t, QPoint(x, y), self)

    def _add_setting(self, name, value, constant=False):
        self.settings[name] = Setting(name, value, constant, self)

    def bg(self):
        return self._bg_color

    def title_bg(self):
        return self._bg_color.light(80)

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

    def pen(self):
        return Block.selected_pen if self.__selected else Block.border_pen

    def _paint(self, p: QPainter):
        self._paint_bg(p)
        self._paint_title(p)
        p.setPen(QPen(self.pen().brush(), 1))
        self._paint_ins(p)
        self._paint_outs(p)
        self._paint_content(p)

    def _paint_bg(self, p: QPainter):
        pen = Block.selected_pen if self.__selected else Block.border_pen
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(pen)
        p.setBrush(self.bg())
        p.drawRoundedRect(Block.padding, Block.padding, self.width() - 2 * Block.padding,
                          self.height() - 2 * Block.padding, 8, 8)
        p.setBrush(self.title_bg())
        p.drawRoundedRect(Block.padding, Block.padding, self.width() - 2 * Block.padding, 35 + Block.padding, 8, 8)
        p.setBrush(self.bg())
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(1 + Block.padding, 35 + Block.padding, self.width() - 2 - 2 * Block.padding, 10)
        p.setPen(pen)
        if self._resizable:
            p.setBrush(pen.brush())
            p.drawPath(self.__corner_path.translated(self.width(), self.height()))

    def _paint_title(self, p: QPainter):
        p.drawLine(Block.padding, 35 + Block.padding, self.width() - Block.padding, 35 + Block.padding)
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

    def _paint_ins(self, p: QPainter):
        for i in self.inputs:
            self.inputs[i].paint(p)

    def _paint_outs(self, p: QPainter):
        for i in self.outputs:
            self.outputs[i].paint(p)

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

    def node(self, p):
        for k in self.inputs:
            i = self.inputs[k]
            if i.contains(p):
                return i
        for k in self.outputs:
            o = self.outputs[k]
            if o.contains(p):
                return o
        return None

    def __create_line(self, n):
        l = n.get_line()
        self.parent().add_line(l)
        return l

    def mousePressEvent(self, e: QMouseEvent):
        self.parent().select(self)
        n = self.node(e.pos())
        if n is not None:
            self.__line = self.__create_line(n)
            self.__action = Action.CONNECTING
            return

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
        elif self.__action == Action.CONNECTING and self.__line is not None:
            p = QPoint(e.x() + self.x(), e.y() + self.y())
            self.__line.update(p)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.__action == Action.CONNECTING and self.__line is not None:
            self.parent().check_line(self.__line)
            self.__line = None
        self.__action = Action.NONE

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        self._double_click()

    def _double_click(self):
        # to be defined in the sub blocks
        return

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

    def setGeometry(self, *__args):
        QWidget.setGeometry(self, *__args)
        self.update_nodes()

    def update_nodes(self):
        x = self.width() - 5 - Block.padding
        for k in self.outputs:
            o = self.outputs[k]
            o.pos.setX(x)
            o.update()
        for k in self.inputs:
            i = self.inputs[k]
            i.update()

    def _corner_path(self):
        return self.__corner_path


class WidgetBlock(Block):
    def __init__(self, type_name: str, name: str, parent: QWidget=None):
        Block.__init__(self, type_name, name, parent)
        self._widget = None
        self._bg_color = QColor(77, 77, 77, 220)
        self.setMinimumHeight(60)

    def title_bg(self):
        return self._bg_color

    def set_widget(self, w: QWidget):
        self._widget = w
        if self.mode() == Mode.EDIT_LOGIC:
            w.setVisible(False)

    def init_gui_settings(self):
        self.settings['X'] = Setting('X', IntegerValue(5))
        self.settings['Y'] = Setting('Y', IntegerValue(5))
        self.settings['Width'] = Setting('Width', IntegerValue(90, self.minimumWidth()))
        self.settings['Height'] = Setting('Height', IntegerValue(120, self.minimumHeight()))

    def _paint_content(self, p: QPainter):
        Block._paint_content(self, p)
        self._paint_widget(p)

    def _paint_widget(self, p):
        if self._widget is not None:
            p.setClipRect(Block.padding + 5, 5 + Block.padding, self.width() - 2 * Block.padding - 10,
                          25)
            p.translate(self.padding + 5, 5 + self.padding)
            self._widget.render(p, QPoint(), QRegion(), QWidget.IgnoreMask)

    def _paint_title(self, p: QPainter):
        f = p.font()
        f.setBold(True)
        f.setPointSize(8)
        p.setPen(QColor(self._fg_color.red(), self._fg_color.green(), self._fg_color.blue(), 180))
        p.setFont(f)
        p.drawText(QRectF(6 + Block.padding, 25 + Block.padding, self.width() - 12, 15), str(self.name()))

    def _paint_bg(self, p: QPainter):
        pen = self.pen()
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(pen)
        p.setBrush(self.bg())
        p.drawRoundedRect(Block.padding, Block.padding, self.width() - 2 * Block.padding,
                          self.height() - 2 * Block.padding, 8, 8)
        p.setPen(pen)
        if self._resizable:
            p.setBrush(pen.brush())
            p.drawPath(self._corner_path().translated(self.width(), self.height()))


class VariableBlock(Block):
    def __init__(self, name: str="Var", parent=None):
        Block.__init__(self, "Variable", name, parent)
        self._resizable = False
        self._bg_color = QColor(233, 221, 175)
        self._fg_color = QColor(0, 0, 0)
        self.settings["Value"] = Setting('Value', BaseValue(NoneType()))
        self._add_input('Value', NoneType())
        self._add_output('Value', NoneType())

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
            s = str(self.settings["Value"].data())
        p.drawText(QRectF(Block.padding + 5, self.height() / 2 - 5, self.width() - Block.padding * 2 - 10,
                          30), Qt.AlignCenter, s)

    def _double_click(self):
        s = 'None'
        if self.settings["Value"].data() is not None:
            s = str(self.settings["Value"].data())
        text, ok = QInputDialog.getText(self.parent(), 'Set Value',
                                        'Value: ', QLineEdit.Normal,
                                        s)
        if ok:
            if len(text) > 0 and not text == s:
                v = ValueManager.parse(text)
            elif text == s:
                v = self.settings["Value"]
            else:
                v = BaseValue(NoneType())
            self.settings["Value"].set_value(v)
            self.inputs["Value"].change_type(v.type())
            self.outputs["Value"].change_type(v.type())
            self.repaint()