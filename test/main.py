__author__ = 'martino'

from gui.Basics import VariableBlock, WidgetBlock
from gui.EditorGUI import OIMainWindow
from PyQt4.QtGui import QApplication, QPushButton
from core.Managers import BlockManager
from gui.Css_Ui import Button_Ui
import sys

OM = BlockManager

a = QApplication(sys.argv)
w = OIMainWindow()

x = 5
for i in range(0, 4):
    b = VariableBlock(parent=w.editor())
    b.setGeometry(x, 5, 90, 120)
    x += 5 + 90
    w.editor().add_block(b)

b = WidgetBlock('Button', 'W', parent=w.editor())
pb = QPushButton(b)
b.set_widget(pb)
pb.setStyleSheet(Button_Ui)
pb.setGeometry(0, 0, 100, 20)
pb.setText('Test')
b.setGeometry(10, 130, 120, 90)

w.editor().add_block(b)

w.show()

sys.exit(a.exec_())