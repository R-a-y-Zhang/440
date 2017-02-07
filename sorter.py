class Node:
    def __init__(self, obj, value, left=None, right=None):
        self.obj = obj
        self.value = value
        self.right = right
        self.left = left

class SortedList:
    def __Init__(self):
        self.head = None
        self.tail = None
        self.center = None
        self.rightCount = 0
        self.leftCount = 0

    def insert(self, node):
        if not self.center:
            self.center = node
            self.head = node
            self.tail = node
        else:
            while True:
                if node.value == self.center.value:
                    if self.rightCount == self.leftCount: # move to right
                        rightNode = self.center.right
                        rightNode.left = node
                        node.right = rightNode
                        node.left = self.center
                        self.center.right = node
                        self.rightCount += 1

    def pop(self):
        return None

    def query(self, value):
        return None
   
    def remove(self, index):
        None
