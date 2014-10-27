__author__ = 'martino'

from core.BlockDef import BlockDef
from gui.Basics import Block
from gui.Containers import EditorContainer
from PyQt4.QtGui import QApplication
import sys

a = QApplication(sys.argv)
w = EditorContainer()
w.setMinimumSize(400, 400)
w.setWindowTitle('Test window')

x = 5
for i in range(0, 4):
    bd = BlockDef("TestBlock", "My block.pippo.10")
    b = Block(bd, parent=w)
    b.setGeometry(x, 5, 90, 120)
    x += 5 + 90
    w.add_block(b)


w.show()

sys.exit(a.exec_())