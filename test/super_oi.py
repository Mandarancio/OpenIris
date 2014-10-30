__author__ = 'martino'
from core.Definitions import *
from PyQt4.QtGui import QApplication
import sys

a = QApplication(sys.argv)

test = Container('Test', None)
val = BlockDefinition('Value', 'Test', test)
test.add_block(val)

w = test.get_widget()
w2 = test.get_widget()
w.show()
w.setFixedSize(500, 500)
w2.show()
w2.setFixedSize(500, 500)

sys.exit(a.exec_())