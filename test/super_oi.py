__author__ = 'martino'
from core.Definitions import *
from PyQt4.QtGui import QApplication
import sys

a = QApplication(sys.argv)

test = Container('Test', None)
val = BlockDefinition('Value', 'Test', test)
test.add_block(val)

w = test.get_widget()
w.show()

sys.exit(a.exec_())