__author__ = 'martino'
from PyQt4.QtGui import QWidget, QPalette, QColor, QPainter, QPaintEvent, QKeyEvent
from PyQt4.Qt import QPoint, Qt
from core.Managers import BlockManager
from core.Utils import Mode
from gui.Basics import Label, Input


class Container:
    def __init__(self, parent=None):
        self.blocks = []
        self.lines = []
        self.__parent = parent
        self.__mode = Mode.EDIT_LOGIC

    def add_block(self, block):
        if not block in self.blocks:
            self.blocks.append(block)
            BlockManager.add_block(block)
            block.set_mode(self.__mode)

    def mode(self):
        return self.__mode

    def set_mode(self, mode):
        if mode == self.__mode:
            return
        self.__mode = mode
        for b in self.blocks:
            b.set_mode(mode)

    def select(self, block):
        BlockManager.deselect_all()
        self.deselect_all_lines()
        if block in self.blocks:
            block.select()

    def add_line(self, line):
        if not line in self.lines:
            self.lines.append(line)
            line.set_w_parent(self)

    def remove_line(self, line):
        if line in self.lines:
            self.lines.remove(line)

    def get_node(self, p):
        for b in self.blocks:
            if b.geometry().contains(p):
                p1 = QPoint(p.x() - b.x(), p.y() - b.y())
                n = b.node(p1)
                if n is not None:
                    return n
        return None

    def check_line(self, line):
        p = line.p2
        for b in self.blocks:
            if b.geometry().contains(p):
                p1 = QPoint(p.x() - b.x(), p.y() - b.y())
                n = b.node(p1)
                if n is not None and n.compatible(line.n1) and line.n1.compatible(n):
                    line.connect(n)
                    return
        line.remove()

    def delete_label(self, l: Label):
        if l is not None:
            l.destroy()
            del l

    def create_label(self, name, n):
        return None

    def get_line(self, p: QPoint):
        if self.__mode == Mode.EDIT_GUI or self.__mode == Mode.RUN:
            return None
        for l in self.lines:
            path = l.path()
            if path.contains(p):
                return l
        return None

    def get_selected_lines(self):
        ll = []
        for l in self.lines:
            if l.selected:
                ll.append(l)
        return ll

    def deselect_all_lines(self):
        for l in self.lines:
            l.selected = False

    def delete_block(self, b):
        if b in self.blocks:
            self.blocks.remove(b)
            b.delete()
            BlockManager.remove_block(b)
            b.deleteLater()

    def delete_selected_elements(self):
        bb = BlockManager.get_selected()
        for b in bb:
            self.delete_block(b)
        ll = self.get_selected_lines()
        for l in ll:
            l.remove()


class ContainerWidget(QWidget, Container):
    def __init__(self, parent: QWidget=None):
        QWidget.__init__(self, parent)
        Container.__init__(self)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()

    def add_line(self, line):
        Container.add_line(self, line)
        self.repaint()

    def paintEvent(self, e: QPaintEvent):
        QWidget.paintEvent(self, e)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for l in self.lines:
            l.paint(p)

    def check_line(self, line):
        Container.check_line(self, line)
        self.repaint()

    def delete_label(self, l: Label):
        if l is not None:
            l.deleteLater()

    def create_label(self, name, n):
        l = Label(name, n, self)
        x = n.abs_pos().x() + 10
        if isinstance(n, Input):
            x = n.abs_pos().x() - 10 - l.width()

        if x < 0:
            x = 0
        elif x + l.width() > self.width():
            x = self.width() - l.width()

        l.setGeometry(x, n.abs_pos().y() - l.height() / 2, l.width(), l.height())
        l.show()
        return l

    def deselect_all_lines(self):
        Container.deselect_all_lines(self)
        self.repaint()

    def keyPressEvent(self, e: QKeyEvent):
        print('here')
        if e.key() == Qt.Key_Delete:
            self.delete_selected_elements()
            self.repaint()


class EditorContainer(ContainerWidget):
    def __init__(self, parent: QWidget=None):
        ContainerWidget.__init__(self, parent)
        pal = QPalette(self.palette())
        self.setMinimumSize(250, 250)
        pal.setColor(QPalette.Background, QColor(55, 50, 47))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        # TODO add grid settings and grid view
        # TODO add modes

    def mousePressEvent(self, e):
        self.setFocus()
        BlockManager.deselect_all()
        self.deselect_all_lines()
        l = self.get_line(e.pos())
        if l is not None:
            l.selected = True
            self.repaint()
