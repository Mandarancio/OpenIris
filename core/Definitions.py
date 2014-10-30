__author__ = 'martino'
from core.Settings import Setting
from core.UValue import StringValue, BaseValue, FloatValue
from core.Managers import BlockManager
from core.Types import Type
from PyQt4.QtCore import pyqtSignal, QObject, QRect
from gui.OIBlocks import *
from gui.OIContainers import ContainerWidget


class Container(QObject):
    update = pyqtSignal()
    block_added = pyqtSignal(object)
    block_removed = pyqtSignal(object)

    def __init__(self, name: str, parent=None):
        QObject.__init__(self, parent)
        self.blocks = []
        self.lines = []
        self.__name = name
        self.__parent = parent

    def name(self):
        return self.__name

    def add_block(self, b):
        if b not in self.blocks:
            b.set_parent(self)
            self.blocks.append(b)
            BlockManager.add_block(b)
            self.block_added.emit(b)

    def remove_block(self, b):
        if b in self.blocks:
            self.blocks.remove(b)
            BlockManager.remove_block(b)
            b.disconnect_all()
            self.block_removed.emit(b)

    def add_line(self, l):
        if l not in self.lines:
            self.lines.append(l)
            self.update.emit()

    def remove_line(self, l):
        if l in self.lines:
            self.lines.remove(l)
            self.update.emit()

    def get_super_parent(self):
        if self.__parent is not None:
            return self.__parent.get_super_parent()
        else:
            return self

    def get_widget(self, parent=None):
        return ContainerWidget(self, parent)


class Node(QObject):
    update = pyqtSignal()
    data_received = pyqtSignal(object, BaseValue)

    def __init__(self, name: str, t: Type, parent):
        QObject.__init__(self, parent)
        self.__parent = parent
        self.__name = name
        self.__type = t
        self.__connections = []
        self.__lines = []

    def parent(self):
        return self.__parent

    def name(self):
        return self.__name

    def type(self):
        return self.__type

    def lines(self):
        return self.__lines

    def compatible(self, node):
        if node is None or node is self or node.__class__ == self.__class__ or node in self.__connections:
            return False
        if node.type().compatible(self.__type) and self.__type.compatible(node.type()):
            return True
        return False

    def connect_to(self, node, line=None):
        self.__connections.append(node)
        if line is not None:
            self.__lines.append(line)
        self.update.emit()

    def find_line(self, node):
        for l in self.__lines:
            if l.has_node(node):
                return l
        return None

    def remove_line(self, line):
        if line not in self.__lines:
            self.__lines.remove(line)
        self.update.emit()

    def add_line(self, line):
        if line is not None and line not in self.__lines:
            self.__lines.append(line)
        self.update.emit()

    def disconnect_from(self, node):
        if node in self.__connections:
            l = self.find_line(node)
            if l is not None:
                self.__lines.remove(l)
            self.__connections.remove(node)
            self.update.emit()

    def get_line(self):
        return None


class Line:
    def __init__(self, b1: Node):
        self.__b1 = b1
        b1.add_line(self)
        self.__b2 = None

    def has_node(self, n):
        return self.__b1 == n or self.__b2 == n

    def get_other(self, n):
        if self.has_node(n):
            if n == self.__b1:
                return self.__b2
            else:
                return self.__b1
        return None

    def connect(self, b2: Node):
        self.__b2 = b2
        b2.connect_to(self.__b1, self)
        self.__b1.connect_to(b2)

    def delete(self):
        if self.__b2 is not None:
            self.__b1.disconnect_from(self.__b2)
            self.__b2.disconnect_from(self.__b1)
        else:
            self.__b1.remove_line(self)


class Input(Node):
    def __init__(self, name: str, t: Type, parent):
        Node.__init__(self, name, t, parent)

    def value_received(self, parent, data: BaseValue):
        self.data_received(parent, data)

    def connect_to(self, node, line=None):
        Node.connect_to(self, node, line)
        node.data_recived.connect(self.value_received)

    def disconnect_from(self, node):
        Node.disconnect_from(self, node)
        node.data_recived.disconnect(self.value_received)

    def get_line(self):
        if len(self.lines()) > 0:
            l = self.lines()[len(self.lines()) - 1]
            self.disconnect_from(l.get_other(self))
            return l
        else:
            l = Line(self)
            self.add_line(l)
            return l


class Output(Node):
    def __init__(self, name: str, t: Type, parent):
        Node.__init__(self, name, t, parent)

    def send_data(self, data: BaseValue):
        self.data_received.emit(self.parent(), data)

    def get_line(self):
        l = Line(self)
        self.add_line(l)
        return l


class BlockDefinition(QObject):
    selected = pyqtSignal(bool)
    changed_setting = pyqtSignal(Setting)
    repaint = pyqtSignal()

    def __init__(self, type_name: str, name: str, parent: Container):
        QObject.__init__(self, parent)
        self.settings = {'Name': Setting('Name', StringValue(name))}
        self.inputs = {}
        self.outputs = {}
        self.trig_in = {}
        self.trig_out = {}
        self._parent = parent
        self._type = type_name
        self._selected = False
        self.init_settings()

    def init_settings(self):
        s = Setting('X', FloatValue(.0))
        self.__add_setting(s)
        s = Setting('Y', FloatValue(.0))
        self.__add_setting(s)
        s = Setting('Width', FloatValue(0.9))
        self.__add_setting(s)
        s = Setting('Height', FloatValue(1.2))
        self.__add_setting(s)

    def __add_setting(self, s):
        self.settings[s.name()] = s

    def name(self):
        return self.settings['Name'].data()

    def updated(self):
        self.repaint.emit()

    def add_input(self, inp: Input):
        self.inputs[inp.name()] = inp
        inp.update.connect(self.updated)

    def add_output(self, output: Output):
        self.outputs[output.name()] = output
        output.update.connect(self.updated)

    def disconnect_all(self):
        for k in self.inputs:
            self.inputs[k].deconnect_all()
        for k in self.outputs:
            self.outputs[k].deconnect_all()

    def set_setting(self, name, data):
        if name in self.settings:
            s = self.settings[name]
            s.set_data(data)
            self.changed_setting.emit(s)

    def get_setting(self, name):
        if name in self.settings:
            return self.settings[name].data()
        return None

    def type_name(self):
        return self._type

    def is_selected(self):
        return self._selected

    def select(self):
        self._selected = True
        self.selected.emit(self._selected)

    def deselect(self):
        self._selected = False
        self.selected.emit(self._selected)

    def parent_container(self):
        return self._parent

    def set_parent(self, p: Container):
        self._parent = p

    def get_widget(self, cont):
        return OIBlock(self, cont)
	
    def get_geometry(self, dpi=1.0):
        x=self.get_setting('X')*dpi
        y=self.get_setting('Y')*dpi
        w=self.get_setting('Width')*dpi
        h=self.get_setting('Height')*dpi
        return QRect(round(x),round(y),round(w),round(h))

