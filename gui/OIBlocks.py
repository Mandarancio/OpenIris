__author__ = 'martino'
from PyQt4.QtGui import QWidget, QPainter, QColor, QPen, QPaintEvent, QMouseEvent
from PyQt4.QtCore import QRectF, QPoint, Qt
from core.Utils import Info


class OINode:
    def __init__(self, pos: QPoint, node):
        self.__node = node
        self.pos = pos
        self.size = 9
        self.lines = []

    def type(self):
        return self.__node.type()

    def paint(self, p: QPainter):
        p.setBrush(self.type().color())
        p.drawEllipse(self.pos.x(), self.pos.y(), self.size, self.size)
        if len(self.lines) > 0:
            pen = p.pen()
            p.setBrush(self.type().color().darker())
            p.setPen(QColor(0, 0, 0, 0))
            p.drawEllipse(self.pos.x() + 2, self.pos.y() + 2, self.size - 4, self.size - 4)
            p.setPen(pen)


class OIBlock(QWidget):
    border_color = QColor(137, 117, 89)
    border_pen = QPen(border_color, 2)
    selected_pen = QPen(border_color.lighter().lighter(), 2)
    padding = 0.05

    def __init__(self, block, parent):
        QWidget.__init__(self, parent)
        self.__nodes = []
        self.__block = block
        self._resizable = False
        self.__block.repaint.connect(self.repaint)
        self._bg_color = QColor(159, 160, 144, 255)
        self._fg_color = QColor(255, 255, 255)
        self.setGeometry(block.get_geometry(Info.dpi))

        block.selected.connect(self.repaint)

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
        # p.setPen(QPen(self.pen().brush(), 1))
        # self._paint_ins(p)
        # self._paint_outs(p)
        # self._paint_content(p)

    def pen(self):
        return OIBlock.selected_pen if self.selected() else OIBlock.border_pen

    def _paint_bg(self, p: QPainter):
        pen = self.pen()
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(pen)
        p.setBrush(self.bg())
        p.drawRoundedRect(OIBlock.padding, OIBlock.padding, self.width() - 2 * OIBlock.padding,
                          self.height() - 2 * OIBlock.padding, 8, 8)
        p.setBrush(self.title_bg())
        p.drawRoundedRect(OIBlock.padding, OIBlock.padding, self.width() - 2 * OIBlock.padding, 35 + OIBlock.padding, 8,
                          8)
        p.setBrush(self.bg())
        p.setPen(QColor(0, 0, 0, 0))
        p.drawRect(1 + OIBlock.padding, 35 + OIBlock.padding, self.width() - 2 - 2 * OIBlock.padding, 10)
        p.setPen(pen)
        if self._resizable:
            p.setBrush(pen.brush())
            p.drawPath(self.__corner_path.translated(self.width(), self.height()))

    def _paint_title(self, p: QPainter):
        p.drawLine(OIBlock.padding, 35 + OIBlock.padding, self.width() - OIBlock.padding, 35 + OIBlock.padding)
        p.setPen(self._fg_color)
        f = p.font()
        f.setPointSize(10)
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRectF(4 + OIBlock.padding, OIBlock.padding + 2, self.width() - 12, 25),
                   str(self.__block.name()))
        f.setBold(False)
        f.setPointSize(8)
        p.setPen(QColor(self._fg_color.red(), self._fg_color.green(), self._fg_color.blue(), 100))
        p.setFont(f)
        p.drawText(QRectF(4 + OIBlock.padding, 18 + OIBlock.padding, self.width() - 12, 15),
                   str(self.__block.type_name()))

    def _paint_ins(self, p: QPainter):
        return

    def _paint_outs(self, p: QPainter):
        return

    def _paint_content(self, p: QPainter):
        # nothing to do
        return

    def paintEvent(self, e: QPaintEvent):
        if e.isAccepted():
            p = QPainter(self)
            self._paint(p)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.__block.select()
            print('here')
