__author__ = 'martino'
from core.BlockDef import BlockDef
from PyQt4.QtGui import QWidget, QPainter, QPaintEvent, QPen, QColor


class Block(QWidget):
    border_color = QColor(55, 55, 55)
    border_pen = QPen(border_color, 2)

    def __init__(self, b_def: BlockDef, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.__def = b_def
        self.setMinimumSize(90, 120)

    def paintEvent(self, e: QPaintEvent):
        if e.isAccepted():
            p = QPainter(self)
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
