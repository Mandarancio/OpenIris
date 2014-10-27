__author__ = 'martino'


def remove_index(name):
    i = name.find('.')
    if i < 0 or i >= len(name) - 1:
        return str(name)
    index = i
    while index != -1:
        i = index
        index = name.find('.', i+1)

    if name[i + 1] >= '0' and name[i + 1] <= '9':
        return name[:i]
    return name


class BlockManager:
    objects = []

    @staticmethod
    def add_block(block):
        if not block in BlockManager.objects:
            block.settings()["Name"].set_data(BlockManager.__check_name(block.settings()["Name"].data()))
            BlockManager.objects.append(block)

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
            if remove_index(o.settings()["Name"].data()) == n:
                i += 1
        n += '.' + str(i)
        return n
