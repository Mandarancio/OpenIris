__author__ = 'martino'
# from core.Definitions import *
from core.Utils import Info
from core.Managers import BlockManager
from core.Definitions import Container
from gui.OIWorkSpace import OIWorkSpace
from PyQt4.QtGui import QApplication  # , QWidget, QGridLayout
import sys

a = QApplication(sys.argv)
BlockManager.root = Container('Root')
BlockManager.objects.append(BlockManager.root)
Info.dpi = a.desktop().logicalDpiX()

window = OIWorkSpace()
ws = window
w1 = ws.central_widget().h_split(0.2)
w1.v_split(0.3)
window.show()
#
# print('DPI: ' + str(Info.dpi))
#
# test = Container('Test', None)
# val1 = VariableDefinition(' A', test)
# val2 = VariableDefinition('B', test)
# # val.settings['X'].set_data(-100)
# test.add_block(val1)
# test.add_block(val2)
#
# mw = QWidget()
# mw.setWindowTitle('OpenIris')
# mw.setGeometry(0, 0, 800, 400)
# l = QGridLayout(mw)
# mw.setLayout(l)
#
# w1 = test.get_widget(mw)
# w2 = test.get_widget(mw)
# l.setMargin(0)
# l.setSpacing(1)
# l.addWidget(w1, 0, 0)
# l.addWidget(w2, 0, 1)
# mw.show()
# w2.show()

sys.exit(a.exec_())

