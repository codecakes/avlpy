#!/usr/bin/env python

from collections import deque

# Individual Node operations
def findMax(node):
    while node.hasRightChild():
        node = node.rightChild
    return node

def findMin(node):
    while node.hasLeftChild():
        node = node.leftChild
    return node


class TreeNode(object):
    def __init__(self,key,val,left=None,right=None,parent=None):
        self.key = key
        self.val = val
        if isinstance(left, TreeNode):
            if left.key <= self.key:
                self.leftChild = left
        else: self.leftChild = None
        if isinstance(right, TreeNode):
            if right.key > self.key:
                self.rightChild = right
        else: self.rightChild = None
        self.parent = parent

    def hasLeftChild(self): return self.leftChild

    def hasRightChild(self): return self.rightChild

    def isLeftChild(self):
        if self.parent: return self.parent.leftChild == self
        return False

    def isRightChild(self):
        if self.parent: return self.parent.rightChild == self
        return False

    def isRoot(self): return not self.parent

    def isLeaf(self): return not (self.rightChild or self.leftChild)

    #def hasChildren(self):
    #    return self.rightChild and self.leftChild

    def setParentChild(self, newNode):
        '''
        Sets self node's parent's relation to a new child node newNode.
        Sets self's parent to None.
        Removes and parent-self relationship.

        newNode: Could be a Node type or None.
        '''
        if self.parent:
            if self.isLeftChild(): self.parent.leftChild = newNode
            elif self.isRightChild(): self.parent.rightChild = newNode
            self.parent = None

    def removeParent(self, newParent, otherNode=None):
        '''Removes self's old parents and assigs it newParent'''
        parent_child_dir = 'leftChild' if self.isLeftChild() else ('rightChild' if self.isRightChild() else None)
        # Sets self node's parents point to the otherNode
        self.setParentChild(otherNode)
        # Sets self node' parent to newParent
        self.parent = newParent
        if parent_child_dir:
            setattr(newParent, parent_child_dir, self)

    def replaceNodeData(self,key,value):
        self.key = key
        self.val = value

    # All about Next Larger Node
    def max_node_right(self):
        '''Find the root node of the subtree to which this node-> self belongs to'''
        currentNode = self
        while currentNode.isRightChild() and currentNode.parent:
            currentNode = currentNode.parent
        return currentNode.parent

    def min_node_right(self):
        '''Find the left most node/min node on the right subtree of this node -> self'''
        currentNode = self
        return findMin(currentNode.rightChild) if currentNode.hasRightChild() else currentNode

    def next_larger(self):
        '''Find the node with next larger key'''
        currentNode = self
        return currentNode.max_node_right() if not currentNode.hasRightChild() \
        else currentNode.min_node_right()

    # All about Next Smaller Node
    def max_node_left(self):
        '''Nearest Left Root of the subtree in which the self is'''
        currentNode = self
        while currentNode.isLeftChild() and currentNode.parent:
            currentNode = currentNode.parent
        return currentNode.parent

    def min_node_left(self):
        '''Largest/Max node on the left Subtree of the Node is the next smaller node to self node'''
        currentNode = self
        return findMin(currentNode.leftChild) if currentNode.hasLeftChild() else currentNode

    def next_smaller(self):
        '''Find the node that is next smaller to self node'''
        currentNode = self
        return currentNode.max_node_left() if not currentNode.hasLeftChild() \
        else currentNode.min_node_left()


#BST functions
def swap(node1, node2):
    tmp = node1
    node1.replaceNodeData(node2.key, node2.val)
    node2.replaceNodeData(tmp.key, tmp.val)

def destroy(node):
    if node.parent:
        if node.isLeftChild():
            node.parent.leftChild = None
        else:
            node.parent.rightChild = None
    if node.hasLeftChild():
        node.leftChild = None
    if node.hasRightChild():
        node.rightChild = None
    del node

def delMax(bst):
    node = findMax(bst.root)
    print "deleting %s"%(node.key)
    newNode = bst._remove(node)
    return newNode

def delMin(bst):
    node = findMin(bst.root)
    print "deleting %s"%(node.key)
    newNode = bst._remove(node)
    return newNode

def delete(self, node):
    """
    perform removal for bst.
    @param:
        - self: bst Tree
        - node: node to be removed

    Assuming key is not Min or Max.
        - If key is a leaf - just delete
        - If key has one subtree i.e. left subtree - max leaf of left subtree \
        takes key' position
        - If key has two subtrees OR right subtree:
                - find Min node of right subtree
                - swap Min node with key.
                - delete key
    """
    parent = node.parent
    if node.isLeaf():
        if not parent: self.root = None
        node.setParentChild(None)
        del node
        return parent

    if node.hasLeftChild() and not node.hasRightChild():
        newNode = node.min_node_left()
    elif node.hasRightChild():
        newNode = node.next_larger()
    swap(node, newNode)
    destroy(newNode)
    if not parent: self.root = node
    else: node.parent = parent
    del newNode
    return node



class BinarySearchTree(object):

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self): return self.size

    # Find/Search operation
    def get(self,key):
       if self.root:
           return self._get(key,self.root)
       return None

    def _get(self,key,currentNode):
        while currentNode:
            if key == currentNode.key: return currentNode
            elif key < currentNode.key: currentNode = currentNode.leftChild
            else: currentNode = currentNode.rightChild
        return None

    def __getitem__(self,key): return self.get(key)

    def __contains__(self,key): return not not self.get(key)

    def __iter__(self):
        '''bfs type level order traversal'''
        if self.root:
            s = deque([self.root], 3)
            while s:
                node = s.pop()
                yield node
                if node.hasLeftChild(): s.appendleft(node.leftChild)
                if node.hasRightChild(): s.appendleft(node.rightChild)
        return

    # insert operation
    def insert(self,key,val, nodeClass=TreeNode, left=None, right=None):
        if self.root:
            node = self._insert(key,val, self.root, nodeClass, left=left, right=right)
        else:
            node = self.root = nodeClass(key,val)
        self.size = self.size + 1
        return node

    def _insert(self,key,val, currentNode, nodeClass, left=None, right=None):
        lastNode = None
        child_attr = ''
        while currentNode:
            lastNode = currentNode
            if key <= currentNode.key:
                currentNode = currentNode.leftChild
                child_attr = 'leftChild'
            else:
                currentNode = currentNode.rightChild
                child_attr = 'rightChild'
        setattr(lastNode, child_attr, nodeClass(key,val,left=left, right=right, parent=lastNode))
        return getattr(lastNode, child_attr)

    def __setitem__(self, key, val):
        return self.insert(key, val)

    def _remove(self, node):
        if node:
            node = delete(self, node)
            self.size -= 1

    # delete operation
    def __delitem__(self, key):
        node = self[key]
        self._remove(node)
        # Returns either None if node Key not found or the newly replaced node in its position
        return node

# avlNode functions
def update_height(node):
        left_height = node.leftChild.height if node.hasLeftChild() else -1
        right_height = node.rightChild.height if node.hasRightChild() else -1
        # print "height is %s"%(max(left_height, right_height) + 1)
        node.height = max(left_height, right_height) + 1
        return

class avlNode(TreeNode):
    '''height is the invariant'''

    def __init__(self,key,val,left=None,right=None,parent=None):
        super(type(self), self).__init__(key,val,left=left,right=right,parent=parent)
        update_height(self)


#AVL tree helper functions
def rotateRight(avl, node):
    # print "Rotating Node %s to right" %(node.key)
    pivot = node.leftChild
    if not pivot:
        raise ValueError("New Pivot Node not present!")

    # node-child transformation
    node.leftChild = pivot.rightChild
    if node.hasLeftChild():
        node.leftChild.parent = node

    # node-node transformation
    pivot.rightChild = node

    # parent-node transformation
    pivot.parent = node.parent
    if node.isRoot():
        avl.root = pivot
    elif node.isLeftChild():
        pivot.parent.leftChild = pivot
    else:
        pivot.parent.rightChild = pivot
    node.parent = pivot

    # update height post rotation
    update_height(node)
    update_height(pivot)
    return pivot

def rotateLeft(avl, node):
    # print "Rotating Node %s to left" %(node.key)
    pivot = node.rightChild
    if not pivot:
        raise ValueError("New Pivot Node not present!")

    # node-child transformation
    node.rightChild = pivot.leftChild
    if node.hasRightChild():
        node.rightChild.parent = node

    # node-node transformation
    pivot.leftChild = node

    # parent-node transformation
    pivot.parent = node.parent
    if node.isRoot():
        avl.root = pivot
    elif node.isLeftChild():
        pivot.parent.leftChild = pivot
    else:
        pivot.parent.rightChild = pivot
    node.parent = pivot

    # update height post rotation
    update_height(node)
    update_height(pivot)
    return pivot

def height(node):
    '''Returns height or if its a mythical one, returns -1'''
    if node is None:
        return -1
    else:
        return node.height

def rebalance(avl, node):
    '''Main avlTree property stabalization function'''
    currentNode = node
    # print "inside rebalance"
    while currentNode:
        update_height(currentNode)
        # print "node is %s updated height %s"%(currentNode.key, currentNode.height)
        # LEFT HEAVY
        if height(currentNode.leftChild) - height(currentNode.rightChild) > 1:
            if ( height(currentNode.leftChild.rightChild) > height(currentNode.leftChild.leftChild) ):
                rotateLeft(avl, currentNode.leftChild)
            rotateRight(avl, currentNode)
        # RIGHT HEAVY
        elif height(currentNode.rightChild) - height(currentNode.leftChild) > 1:
            if ( height(currentNode.rightChild.leftChild) > height(currentNode.rightChild.rightChild) ):
                rotateRight(avl, currentNode.rightChild)
            rotateLeft(avl, currentNode)

        currentNode = currentNode.parent
        # if currentNode: print "node's parent=%s"%(currentNode.key)

def avlDelMax(avl):
    newNode = delMax(avl)
    if newNode:
        rebalance(avl, newNode)

def avlDelMin(avl):
    newNode = delMin(avl)
    if newNode:
        rebalance(avl, newNode)


class avlTree(BinarySearchTree):

    def __init__(self):
        super(type(self), self).__init__()

    # insert operation
    def __setitem__(self, key, val):
        return self.insert(key, val)

    def insert(self,key,val, nodeClass=avlNode, left=None, right=None):
        node = super(type(self), self).insert(key,val, nodeClass=nodeClass, left=left, right=right)
        # if node.parent:
        #     node.parent.height = update_height(node.parent)
        rebalance(self, node)

    # delete operation
    def __delitem__(self, key):
        node = super(type(self), self).__delitem__(key)
        rebalance(self, node)



if __name__ == "__main__":
    print "\ntesting for BinarySearchTree"

    b = BinarySearchTree()

    b.insert(1, 'red')
    assert b.size == 1

    b.insert(20, 'redness')
    assert b.size == 2

    b.insert(40, 'hotness')
    assert b.size == 3

    for x in b:
        print x.key, x.val
    print "="*10

    print "deleting b[1]"
    del b[1]
    assert b.size == 2

    for x in b:
        print x.key, x.val
    print "="*10

    b.insert(40, 'hotness')
    b.insert(40, 'hotness')
    b.insert(400, 'hotness')
    b.insert(-34540, 'hotness')
    assert b.size == 6

    for x in b:
        print x.key, x.val
    print "="*10

    print "\ntesting for avlTree"

    r = avlTree()
    print "\ntesting for insertion"
    r[1] = 'one'
    r[3] = 'three'
    r[2] = 'two'
    r[4] = 'four'
    r[6] = 'six'
    r[5] = 'five'
    assert r.root.key == 4
    assert r.size == 6

    for x in r:
        print x.key, x.val
    print "="*10

    # print "Creating new avlTree\n"
    # r = avlTree()
    # print "\n randomly generated integers"
    # arr = [ 27552,  29086,  70311, -84170,  13924,   9010,  75356, -14113, 15858, -26237]
    # for each in arr: r[each] = each

    print "\n testing for delMax and delMin"
    del_stat = [0, 1, 0, 1, 0, 1]

    assert r.root != None
    for each in del_stat:
        if each:
            avlDelMax(r)
            print "avlDelMax done"
        else:
            avlDelMin(r)
            print "avlDelMin done"
        print "="*5, "listing nodes","="*5
        for x in r:
            print x.key, x.val
        "="*10
    assert r.root == None



