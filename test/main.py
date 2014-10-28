__author__ = 'martino'

from gui.Basics import VariableBlock, WidgetBlock
from gui.Containers import EditorContainer
from PyQt4.QtGui import QApplication, QPushButton
from core.Managers import BlockManager
import sys

OM = BlockManager

a = QApplication(sys.argv)
w = EditorContainer()
w.setMinimumSize(400, 400)
w.setWindowTitle('Test window')


x = 5
for i in range(0, 4):
    b = VariableBlock(parent=w)
    b.setGeometry(x, 5, 90, 120)
    x += 5 + 90
    w.add_block(b)

b = WidgetBlock('W', 'W', parent=w)
pb = QPushButton(b)
pb.setGeometry(0, 0, 100, 20)
pb.setText('Test')
b.set_widget(pb)

w.add_block(b)

w.show()

sys.exit(a.exec_())