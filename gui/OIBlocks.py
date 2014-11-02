__author__ = 'martino'
from PyQt4.QtGui import QWidget, QPainter, QColor, QPen, QPaintEvent, QMouseEvent, QPainterPath, \
    QGraphicsDropShadowEffect
from PyQt4.QtCore import QRectF, QPointF, Qt, QPoint
from core.Utils import Info, Mode, Action, Alignment


class OINode:
    def __init__(self, pos: QPointF, a: Alignment, node):
        self.__node = node
        self.pos = pos
        self.size = 0.09
        self.alignment = a
        self.lines = []

    def type(self):
        return self.__node.type()

    def paint(self, p: QPainter):
        t = self.__node.type()
        p.setBrush(self.__node.type().color())
        p.drawEllipse(round(self.pos.x() * Info.dpi), round(self.pos.y() * Info.dpi), round(self.size * Info.dpi),
                      round(self.size * Info.dpi))
        # if len(self.lines) > 0:
        # pen = p.pen()
        # p.setBrush(self.type().color().darker())
        # p.setPen(QColor(0, 0, 0, 0))
        # p.drawEllipse(self.pos.x() + 2, self.pos.y() + 2, self.size - 4, self.size - 4)
        # p.setPen(pen)

    def real_pos(self):
        x = round(self.pos.x() * Info.dpi)
        y = round(self.pos.y() * Info.dpi)
        return QPoint(x, y)

    def contains(self, p: QPoint):
        d = self.size * Info.dpi
        pos = self.real_pos()
        dx = pos.x() - p.x()
        dy = pos.y() - p.y()
        if dx * dx + dy * dy <= d * d:
            return True
        return False


class OIBlock(QWidget):
    border_color = QColor(137, 117, 89)
    padding = 0.05
    radius = 0.08

    def __init__(self, block, parent):
        QWidget.__init__(self, parent)
        self.__nodes = []
        self.__block = block
        self._resizable = True
        self.__block.repaint.connect(self.repaint)
        self._bg_color = QColor(159, 160, 144, 255)
        self._fg_color = QColor(255, 255, 255)
        self.setGeometry(block.get_geometry(Info.dpi))
        self.__action = Action.NONE
        self.__status = Mode.EDIT_LOGIC
        self.__corner_path = None
        self.__origin = None
        self.__translation = QPoint()
        if self._resizable:
            self.__init_corner()
        self.__init_nodes()
        self.__init_listeners()
        self.setMouseTracking(True)

    def __init_nodes(self):
        y = .45
        x = .01
        for k in self.__block.inputs:
            i = self.__block.inputs[k]
            n = OINode(QPointF(x, y), Alignment.Left, i)
            self.__nodes.append(n)
            y += 0.05 + n.size
        x = self.width() / Info.dpi - .12
        y = 0.45
        for k in self.__block.outputs:
            o = self.__block.outputs[k]
            n = OINode(QPointF(x, y), Alignment.Right, o)
            self.__nodes.append(n)
            y += .05 + n.size

    def __init_listeners(self):
        self.__block.selected.connect(self.select)
        self.__block.settings['Width'].value_update.connect(self.geometry_update)
        self.__block.settings['Height'].value_update.connect(self.geometry_update)
        self.__block.settings['X'].value_update.connect(self.geometry_update)
        self.__block.settings['Y'].value_update.connect(self.geometry_update)

    def select(self, val: bool):
        if val:
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(20)
            effect.setXOffset(0)
            effect.setYOffset(0)
            effect.setColor(QColor(0, 0, 0, 180))
            self.setGraphicsEffect(effect)
            self.raise_()
        else:
            eff = self.graphicsEffect()
            del eff
            self.setGraphicsEffect(None)

    def geometry_update(self):
        r = self.__block.get_geometry(Info.dpi)
        r.translate(self.__translation)
        self.setGeometry(r)
        self.__update_nodes()

    def __update_nodes(self):
        x = self.width() / Info.dpi - .12
        for n in self.__nodes:
            if n.alignment == Alignment.Right:
                y = n.pos.y()
                n.pos = QPointF(x, y)
        self.repaint()

    def selected(self):
        return self.__block.is_selected()

    def bg(self):
        return self._bg_color

    def title_bg(self):
        return self._bg_color.light(80)

    def block(self):
        return self.__block

    def _paint(self, p: QPainter):
        self._paint_bg(p)
        self._paint_title(p)
        p.setPen(QPen(self.pen().brush(), 0.01 * Info.dpi))
        self._paint_nodes(p)
        # self._paint_outs(p)
        # self._paint_content(p)

    def pen(self):
        p = QPen(OIBlock.border_color.lighter().lighter() if self.selected() else OIBlock.border_color, .02 * Info.dpi)
        return p

    def _paint_bg(self, p: QPainter):
        dpi = Info.dpi
        pen = self.pen()
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(pen)
        p.setBrush(self.bg())
        p.drawRoundedRect(OIBlock.padding * dpi, OIBlock.padding * dpi, self.width() - 2 * OIBlock.padding * dpi,
                          self.height() - 2 * OIBlock.padding * dpi, OIBlock.radius * dpi, OIBlock.radius * dpi)
        p.setBrush(self.title_bg())
        p.drawRoundedRect(OIBlock.padding * dpi, OIBlock.padding * dpi, self.width() - 2 * OIBlock.padding * dpi,
                          .35 * dpi + OIBlock.padding * dpi, OIBlock.radius * dpi,
                          OIBlock.radius * dpi)
        p.setBrush(self.bg())
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(0.01 * dpi + OIBlock.padding * dpi, 0.35 * dpi + OIBlock.padding * dpi,
                   self.width() - 0.02 * dpi - 2 * OIBlock.padding * dpi, 0.10 * dpi)
        p.setPen(pen)
        if self._resizable:
            if self.__corner_path is None:
                self.__init_corner()
            p.setBrush(pen.brush())
            p.drawPath(self.__corner_path.translated(self.width(), self.height()))

    def _paint_title(self, p: QPainter):
        dpi = Info.dpi
        p.drawLine(OIBlock.padding * dpi, 0.35 * dpi + OIBlock.padding * dpi,
                   self.width() - (0.01 + OIBlock.padding) * dpi,
                   0.35 * dpi + OIBlock.padding * dpi)
        p.setPen(self._fg_color)
        f = p.font()
        f.setPointSize(10)
        f.setBold(True)
        p.setFont(f)
        p.drawText(
            QRectF((0.04 + OIBlock.padding) * dpi, (OIBlock.padding + .01) * dpi, self.width() - .12 * dpi, .25 * dpi),
            str(self.__block.name()))
        f.setBold(False)
        f.setPointSize(8)
        p.setPen(QColor(self._fg_color.red(), self._fg_color.green(), self._fg_color.blue(), 100))
        p.setFont(f)
        p.drawText(
            QRectF((.04 + OIBlock.padding) * dpi, (.17 + OIBlock.padding) * dpi, self.width() - .12 * dpi, .15 * dpi),
            str(self.__block.type_name()))

    def __init_corner(self):
        path = QPainterPath()
        dpi = Info.dpi
        path.moveTo(-OIBlock.padding * 1.2 * dpi, (-.15 - OIBlock.padding * 1.2) * dpi)
        path.lineTo((-.15 - OIBlock.padding * 1.2) * dpi, -OIBlock.padding * 1.2 * dpi)
        path.lineTo(-OIBlock.padding * 1.2 * dpi, -OIBlock.padding * 1.2 * dpi)
        path.closeSubpath()
        self.__corner_path = path

    def _paint_nodes(self, p: QPainter):
        for n in self.__nodes:
            n.paint(p)
        return

    def _paint_content(self, p: QPainter):
        # nothing to do
        return

    def paintEvent(self, e: QPaintEvent):
        if e.isAccepted():
            p = QPainter(self)
            self._paint(p)

    def _check_corner(self, pos):
        path = self.__corner_path.translated(self.width(), self.height())
        return path.contains(pos)

    def _check_action(self, action):
        if self.__action != Action.NONE and action != Action.NONE:
            return False
        return True

    def _check_nodes(self, p:QPoint):
        for n in self.__nodes:
            if n.contains(p):
                return n
        return None

    def mousePressEvent(self, e: QMouseEvent):
        self.__block.select()
        n = self._check_nodes(e.pos())
        if n is not None:
            print('Node found')
            return
        if e.button() == Qt.LeftButton:
            if self._resizable:
                if self._check_corner(e.pos()) and self._check_action(Action.RESIZE):
                    self.__origin = e.pos()
                    self.__action = Action.RESIZE
                    self.setCursor(Qt.SizeFDiagCursor)
                    return
            if self._check_action(Action.DRAG):
                self.__origin = e.pos()
                self.__action = Action.DRAG
                self.setCursor(Qt.DragMoveCursor)

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.__action == Action.DRAG:
            dx = e.x() - self.__origin.x()
            dy = e.y() - self.__origin.y()
            self.set_pos(self.x() + dx, self.y() + dy)
        elif self.__action == Action.RESIZE:
            self.set_size(e.x(), e.y())
        else:
            if self._resizable and self.__corner_path.translated(self.width(), self.height()).contains(e.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.__action = Action.NONE
        self.setCursor(Qt.ArrowCursor)

    def set_size(self, w, h):
        w1 = w / Info.dpi
        h1 = h / Info.dpi
        W = self.__block.settings['Width'].value()
        H = self.__block.settings['Height'].value()
        if w1 < W.min:
            w1 = W.min
        elif w1 > W.max:
            w1 = W.max
        if h1 < H.min:
            h1 = H.min
        elif h1 > H.max:
            h1 = H.max

        self.__block.set_setting('Width', w1)
        self.__block.set_setting('Height', h1)

    def set_pos(self, x, y):
        x = x - self.__translation.x()
        y = y - self.__translation.y()
        self.__block.set_setting('X', x / Info.dpi)
        self.__block.set_setting('Y', y / Info.dpi)

    def translate(self, p):
        self.__translation = p
        self.geometry_update()


class OIVariableBlock(OIBlock):
    def __init__(self, block, parent):
        OIBlock.__init__(self, block, parent)
        self._resizable = False
        self._bg_color = QColor(233, 221, 175)
        self._fg_color = QColor(0, 0, 0)