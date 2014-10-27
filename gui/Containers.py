__author__ = 'martino'
from PyQt4.QtGui import QWidget, QPalette, QColor
from core.Managers import BlockManager


class Container:
    def __init__(self, parent=None):
        self.__blocks = []
        self.__parent = parent

    def add_block(self, block):
        if not block in self.__blocks:
            self.__blocks.append(block)
            BlockManager.add_block(block)

    def select(self, block):
        BlockManager.deselect_all()
        if block in self.__blocks:
            block.select()


class EditorContainer(QWidget, Container):
    def __init__(self, parent: QWidget=None):
        QWidget.__init__(self, parent)
        Container.__init__(self)
        pal = QPalette(self.palette())
        pal.setColor(QPalette.Background, QColor(55, 50, 47))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        #TODO add grid settings and grid view
        #TODO add modes

    def mousePressEvent(self, e):
        BlockManager.deselect_all()
