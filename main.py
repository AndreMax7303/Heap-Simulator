from linked_list import LinkedList, Node

HEAP_SIZE = 25


class Program:
    llist = LinkedList(HEAP_SIZE)
    heap_mode = None
    index = {}
    heap = [False] * HEAP_SIZE

    def __init__(self, program_path):
        print(self.llist)
        with open(program_path, 'r') as program:
            lines = program.readlines()
            for line in lines:
                line = line.strip()
                tokens = line.split()
                if tokens[0] == 'heap':
                    self.heap_mode = tokens[1]
                elif tokens[0] == 'exibe':
                    self.print_heap()
                elif tokens[0] == 'new':
                    if self.heap_mode == 'best':
                        self.index[tokens[1]] = self.best_fit(int(tokens[2]))

                    if self.heap_mode == 'worst':
                        self.index[tokens[1]] = self.worst_fit(int(tokens[2]))
                    self.fill_heap(self.index[tokens[1]], int(tokens[2]))

                elif tokens[0] == 'del':
                    if self.has_duplicate(self.index[tokens[1]]):
                        pos = self.index[tokens[1]]
                        self.index.pop(list(self.index.keys())[list(self.index.values()).index(pos)])
                    self.remove_block(self.index[tokens[1]])
                    for i in range(self.index[tokens[1]], self.get_next_index_position(self.index[tokens[1]])):
                        self.heap[i] = False
                    self.index.pop(tokens[1])
                elif tokens[1] == '=':
                    self.index[tokens[0]] = int(self.index[tokens[2]])

    def worst_fit(self, blocks):
        largest = self.llist.head.free_blocks
        position = self.llist.head.position
        for node in self.llist:
            if blocks <= node.free_blocks and node.free_blocks > largest:
                largest = node.free_blocks
                position = node.position

        for node in self.llist:
            if node.position == position:
                node.position += blocks
                node.free_blocks -= blocks
                if node.free_blocks == 0:
                    self.llist.remove(node.position)
                print(node)
                return position

    def best_fit(self, blocks):
        smallest = self.llist.head.free_blocks
        position = self.llist.head.position
        for node in self.llist:
            if blocks <= node.free_blocks <= smallest:
                smallest = node.free_blocks
                position = node.position
        for node in self.llist:
            if node.position == position:
                node.position += blocks
                node.free_blocks -= blocks
                if node.free_blocks == 0:
                    self.llist.remove(node.position)
                return position

    def has_duplicate(self, value):
        count = 0
        for number in self.index.values():
            if number == value:
                count += 1
        return count > 1

    def fill_heap(self, pos, blk):
        for i in range(pos, pos+blk):
            self.heap[i] = True

    def print_heap(self):
        print('HEAP')
        print('POS  | VALUE')
        for i, value in enumerate(self.heap):
            print('%4i | %-5s' % (i, value))
        print('_______________\n')
        print('LIST')
        print(self.llist)
        print('_______________\n')

    def has_space_after(self, index_pos):
        for node in self.llist:
            if node.position > index_pos:
                return True
        return False

    def has_space_before(self, index_pos):
        for node in self.llist:
            if node.position < index_pos:
                return True
        return False

    def is_space_before_close(self, index_pos):
        for node in self.llist:
            if node.position + node.free_blocks == index_pos:
                return True
        return False

    def is_space_after_close(self, index_pos):
        for node in self.llist:
            if index_pos < node.position < self.get_next_index_position(index_pos):
                return True
        return False

    def remove_block(self, block_index):
        if self.has_space_before(block_index) and self.is_space_before_close(block_index):
            for node in self.llist:
                if node.next.position > block_index:
                    node.free_blocks = self.get_next_index_position(block_index) - node.position
                    if node.next is not None:
                        node.next = node.next.next
        elif self.has_space_after(block_index) and self.is_space_after_close(block_index):
            for node in self.llist:
                if node.position < block_index:
                    node.position = block_index
                    node.free_blocks = self.get_next_index_position(block_index) - block_index
        elif self.has_space_before(block_index) and not self.is_space_after_close(block_index):
            for node in self.llist:
                if node.next.position > block_index:
                    new_node = Node(position=block_index,
                                    free_blocks=self.get_next_index_position(block_index)-block_index)
                    new_node.next = node.next
                    node.next = new_node
        else:
            new_node = Node(position=block_index,
                            free_blocks=self.get_next_index_position(block_index) - block_index)
            new_node.next = self.llist.head
            self.llist.head = new_node

    def get_next_index_position(self, index_positon):
        positions = sorted(self.index.values())
        if positions.index(index_positon) == len(positions) - 1:
            return HEAP_SIZE
        else:
            for i, j in enumerate(positions[:-1]):
                if j == index_positon:
                    return positions[i+1]


Program('./program.txt')
