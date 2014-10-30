__author__ = 'martino'

from core.UValue import *


def remove_index(name):
    i = name.find('.')
    if i < 0 or i >= len(name) - 1:
        return str(name)
    index = i
    while index != -1:
        i = index
        index = name.find('.', i + 1)

    if '0' <= name[i + 1] <= '9':
        return name[:i]
    return name


class TypeManager:
    types = []

    @staticmethod
    def add_type(t):
        if t not in TypeManager.types:
            TypeManager.types.append(t)

    @staticmethod
    def get_types():
        return TypeManager.types

    @staticmethod
    def get_type(name):
        for t in TypeManager.types:
            if t.name() == name:
                return t
        return None


class BlockManager:
    objects = []

    @staticmethod
    def name_changed(value, parent):
        print(value.data())
        print(parent.name())

    @staticmethod
    def get_block(name: str):
        for o in BlockManager.objects:
            if o.name() == name:
                return o
        return None

    @staticmethod
    def add_block(block):
        if not block in BlockManager.objects:
            block.settings["Name"].value_update.connect(BlockManager.name_changed)
            block.settings["Name"].set_data(BlockManager.__check_name(block.settings["Name"].data()))
            BlockManager.objects.append(block)

    @staticmethod
    def remove_block(block):
        if block in BlockManager.objects:
            BlockManager.objects.remove(block)

    @staticmethod
    def get_selected():
        sel = []
        for o in BlockManager.objects:
            if o.selected():
                sel.append(o)
        return sel

    @staticmethod
    def deselect_all():
        sel = BlockManager.get_selected()
        for s in sel:
            s.deselect()

    @staticmethod
    def __check_name(name):
        n = name.replace(' ', '_')
        n = remove_index(n)
        i = 0
        for o in BlockManager.objects:
            if remove_index(o.settings["Name"].data()) == n:
                i += 1
        n += '.' + str(i)
        return n


class ValueManager:
    values = {0: IntegerValue, 1: FloatValue, 2: StringValue}

    @staticmethod
    def parse(s: str):
        for k in ValueManager.values:
            o = ValueManager.values[k].parse(s)
            if o is not None:
                return o