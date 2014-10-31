__author__ = 'martino'
from core.Definitions import *
from core.Utils import Info
from PyQt4.QtGui import QApplication, QWidget, QGridLayout
import sys

a = QApplication(sys.argv)

Info.dpi = a.desktop().logicalDpiX()

print('DPI: ' + str(Info.dpi))

test = Container('Test', None)
val = BlockDefinition('Value', 'Test', test)
# val.settings['X'].set_data(-100)
test.add_block(val)


mw = QWidget()
mw.setWindowTitle('OpenIris')
mw.setGeometry(0, 0, 800, 400)
l = QGridLayout(mw)
mw.setLayout(l)

w1 = test.get_widget(mw)
w2 = test.get_widget(mw)
print(w2)
l.setMargin(0)
l.setSpacing(1)
l.addWidget(w1, 0, 0)
l.addWidget(w2, 0, 1)
mw.show()
# w2.show()

sys.exit(a.exec_())

