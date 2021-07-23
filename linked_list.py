import json

class Node:
    def __init__(self, position, free_blocks):
        self.position = position
        self.free_blocks = free_blocks
        self.next = None

    def __repr__(self):
        return '{} : {}'.format(self.position, self.free_blocks)


class LinkedList:
    def __init__(self, size, nodes=None):
        self.head = None
        node = Node(0, size)
        self.head = node

        # if nodes is not None:
        #     node = Node(data=nodes.pop(0))
        #     self.head = node
        #     for elem in nodes:
        #         node.next = Node(data=elem)
        #         node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(json.dumps({'pos': node.position, 'fblk': node.free_blocks}))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def remove(self, position):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.position == position:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.position == position:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception("Node with data '%s' not found" % position)