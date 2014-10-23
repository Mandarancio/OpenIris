__author__ = 'martino'

from core.BlockDef import BlockDef
from gui.Basics import Block
from PyQt4.QtGui import QApplication, QWidget
import sys

a = QApplication(sys.argv)
w = QWidget()
w.setFixedSize(400, 400)
w.setWindowTitle('Test window')

bd = BlockDef("TestBlock", "My block")
b = Block(bd, parent=w)
b.setGeometry(5, 5, 90, 120)

w.show()

sys.exit(a.exec_())