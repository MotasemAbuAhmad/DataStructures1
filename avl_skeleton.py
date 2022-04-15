# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - 204327258
# name2    - elhadperl

import random
'''ik'''

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value, height=0, size=1):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = height

        ### More fields ###
        self.size = size

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    def getSize(self):
        return self.size

    def setSize(self, s):
        self.size = s

    def BFcalc(self):
        return (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(self)

    def hUpdate(self):
        return (lambda n: max(n.getRight().getHeight(), n.getLeft().getHeight()) + 1)(self)

    def sUpdate(self):
        return (lambda n: n.getRight().getSize() + n.getLeft().getSize() + 1)(self)
"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.size = 0
        self.first = None
        self.last = None

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        if self.size == 0:
            return True
        return False

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i, pr=False):
        return self.retrieve_rec(self.root, i + 1, pr).value

    def retrieve_rec(self, node, i, pr=False):
        """edge cases for testing-                                            ### DELETE AFTER ###"""
        if not isinstance(node, AVLNode):
            print("Error: node is not an AVL Node object")                    ### DELETE AFTER ###"""
        if not node.isRealNode():
            print("Error: node is a VR node")                                  ### DELETE AFTER ###"""

        rank = node.getLeft().size + 1
        if rank == i:
            return node
        if i < rank:
            return self.retrieve_rec(node.getLeft(), i)
        else:
            return self.retrieve_rec(node.getRight(), i - rank)

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        counter = 0
        elem = self.initNode(val)             # Initial new node
        if self.empty():                      # Empty list
            self.root = elem
            self.size += 1
            return 0

        if i == self.size:                  # i == len(lst)
            pos = self.appendNode(elem)
        else:
            pos = self.setNode(elem, i)    # Select(self, i+1) == self[i] ==> find the node located in index i
        elem.setParent(pos)
        self.size += 1
        #counter = self.fixUp(pos, False)
        while pos is not None:
            pos.size += 1
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                counter += 1
                if bf == -2 and pos.getRight().BFcalc() == -1:
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and pos.getLeft().BFcalc() == 1:
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp

            else:
                pos = pos.parent

        return counter

    def initNode(self, val):
        elem = AVLNode(val)
        vrNodeR = AVLNode(None, -1, 0)
        vrNodeL = AVLNode(None, -1, 0)
        elem.setRight(vrNodeR)
        elem.setLeft(vrNodeL)
        vrNodeR.setParent(elem)
        vrNodeL.setParent(elem)
        return elem

    def appendNode(self, elem):
        pos = self.root
        while pos.getRight().getHeight() != -1:
            pos = pos.right
        pos.setRight(elem)
        return pos

    def setNode(self, elem, i, pr=False):
        pos = self.retrieve_rec(self.root, i + 1, pr)
        if not pos.left.isRealNode():  # if pos.left is vr
            pos.setLeft(elem)
        else:
            pos = pos.left
            while pos.right.getHeight() != -1:
                pos = pos.right
            pos.setRight(elem)
        return pos

    """ t.l  or t.right          
         \             \
          U     -->     R
           \          /   \
            R   -->  U     E   
          /   \       \
         a     E -->   a        """

    def rotateLeft(self, u, r):
        u.setRight(r.getLeft())    # set-> u[right]= a
        u.getRight().setParent(u)  # set-> a[parent]= u
        r.setLeft(u)               # set-> r[left] = u
        r.setParent(u.getParent()) # set-> r[parent]= t
        u.setParent(r)             # set-> u[parent]= r
        if u is self.root:
            self.root = r
        else:
            # if u is not a root, set his parent to r
            if r.getParent().getRight() == u:
                r.getParent().setRight(r)
            else:
                r.getParent().setLeft(r)
        # Fix size & height
        u.size = u.getLeft().size + u.getRight().size + 1
        u.setHeight((max(u.getRight().getHeight(), u.getLeft().getHeight()) + 1))
        r.size = r.getLeft().size + r.getRight().size + 1
        r.setHeight((max(r.getRight().getHeight(), r.getLeft().getHeight()) + 1))

    def rotateRight(self, u, l):
        u.setLeft(l.getRight())
        u.getLeft().setParent(u)
        l.setRight(u)
        l.setParent(u.getParent())
        u.setParent(l)
        if u is self.root:
            self.root = l
        else:
            if l.getParent().getLeft() == u:
                l.getParent().setLeft(l)
            else:
                l.getParent().setRight(l)
        u.setSize(u.sUpdate())
        u.setHeight(u.hUpdate())
        l.setSize(l.sUpdate())
        l.setHeight(u.hUpdate())

    def fixUp(self, pos, insert=True):
        counter = 0
        while pos is not None:
            pos.size += (lambda act: 1 if insert else -1)(insert)
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                if bf == -2 and (lambda bfc: pos.getRight().BFcalc() == -1 if insert else
                        (pos.getRight().BFcalc() == -1 or pos.getRight().BFcalc() == 0))(insert):
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and (lambda bfc: pos.getLeft().BFcalc() == 1 if insert else
                        (pos.getLeft().BFcalc() == 1 or pos.getLeft().BFcalc() == 0))(insert):
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp

            else:
                pos = pos.parent

        return counter

    """deletes the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        counter = 0
        self.size -= 1
        dNode = self.retrieve_rec(self.root, i + 1)
        # case 1- dNode is a leaf
        if not (dNode.getRight().isRealNode() or dNode.getLeft().isRealNode()):
            pos = self.deleteLeaf(dNode)

        # case 2- dNode has two children
        elif dNode.getRight().isRealNode() and dNode.getLeft().isRealNode():
            sNode = self.findSuccessorD(dNode)  # Find dNode's successor

            if not sNode.getRight().isRealNode() and not sNode.getLeft().isRealNode():
                pos = self.deleteLeaf(sNode)  # case 2.a- sNode is a leaf

            else:  # case 3.b- sNode is a branch
                pos = self.deleteXor(sNode)
            if pos is dNode:  # Edge case- Successor(dNode) == sNode
                pos = sNode
            self.exchangeNodes(dNode, sNode)  # set sNode in dNode location

        else:  # XOR(right(isReal(), left(isReal))
            pos = self.deleteXor(dNode)
        #counter = self.fixUp(pos, False)
        # Fixing up to root
        while pos is not None:
            pos.size -= 1
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                if bf == -2 and (pos.getRight().BFcalc() == -1 or pos.getRight().BFcalc() == 0):
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and (pos.getLeft().BFcalc() == 1 or pos.getLeft().BFcalc() == 0):
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp
            else:
                pos = pos.parent
        if self.size == 0:
            self.root = None
        return counter

    def deleteLeaf(self, dNode):  # not possible- case 2 and dNode == root
        dnp = dNode.getParent()
        if dNode is not self.root:
            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getRight())
                dNode.getRight().setParent(dnp)
            else:
                dnp.setLeft(dNode.getLeft())
                dNode.getLeft().setParent(dnp)
        else:
            self.root = None
        return dnp

    def deleteXor(self, dNode):
        dnp = dNode.getParent()
        if dNode.getRight().isRealNode():
            dNode.getRight().setParent(dnp)
            if dNode is self.root:
                self.root = dNode.getRight()
                return dnp

            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getRight())
            else:
                dnp.setLeft(dNode.getRight())
        else:
            dNode.getLeft().setParent(dnp)
            if dNode is self.root:
                self.root = dNode.getRight()
                return dnp
            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getLeft())
            else:
                dnp.setLeft(dNode.getLeft())
        return dnp

    def exchangeNodes(self, dNode, sNode):
        dnp = dNode.getParent()
        sNode.setParent(dNode.getParent())  # 6.p =none
        sNode.setLeft(dNode.getLeft())
        dNode.getLeft().setParent(sNode)
        if dNode.getRight() is not sNode:
            sNode.setRight(dNode.getRight())
            dNode.getRight().setParent(sNode)
        sNode.setSize(dNode.size)
        if dNode is not self.root:
            if dnp.getRight() is dNode:
                dnp.setRight(sNode)
            else:
                dnp.setLeft(sNode)
        else:
            self.root = sNode

    """
    dNode.setRight(None)
    dNode.setLeft(None)
    dNode.setLeft(None)
    """

    def findSuccessorD(self, pos):
        pos = pos.getRight()
        while pos.getLeft().isRealNode():
            pos = pos.getLeft()
        return pos

    """returns the value of the first item in the list
    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return None

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return None

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        res = [i for i in range(self.size)]
        ### Travel in tree and then add elements by rank as indexes ###
        res1 = []
        return AVLTreeList.ltoa(self, self.root, res1)

        return res

    """real l-to-a func"""

    def ltoa(self, node, res):
        if node is None:
            return
        AVLTreeList.ltoa(self, node.left, res)
        res.append(node.value)
        AVLTreeList.ltoa(self, node.right, res)

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, i):
        return None

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        node = self.root
        return AVLTreeList.goodSearch(self, node, val)

    """Real function for search"""
    """in-order walk through the tree to find requested value"""

    def goodSearch(self, node, val):

        if node is None:
            return -1
        if node.value == val:
            return node.rank

        x = AVLTreeList.goodSearch(node.left, val)
        y = AVLTreeList.goodSearch(node.right, val)
        if x != -1:
            return x
        elif y != -1:
            return y
        else:
            return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        if self.empty():
            return None
        return self.root

    # More functions
    def getSize(self):
        return self.size

    def select(self, i):
        return self.retrieve_rec(self.root, i + 1)

    def rank(self, val):
        return self.search(val)

    ######################################## Put these functions ########################################
    ##################################### inside AVLTreeList class ######################################

    """Checks if the AVL tree properties are consistent

    @rtype: boolean 
    @returns: True if the AVL tree properties are consistent
    """

    def check(self, name):
        print("Checks AVL's tree properties test(input=#", name, "#):")
        if not self.isAVL():
            print("The tree is not an AVL tree!")
        else:
            print("Test 1 ==> Good!")
        if not self.isSizeConsistent():
            print("The sizes of the tree nodes are inconsistent!")
        else:
            print("Test 2 ==> Good!")
        if not self.isHeightConsistent():
            print("The heights of the tree nodes are inconsistent!")
        else:
            print("Test 3 ==> Good!")
        lst = self.nodes()
        rankT = True
        for i in range(self.size):
            if lst[i] != self.retrieve_rec(self.root, i + 1):
                rankT = False
        if rankT:
            print("Test 4 ==> Good!\n")
        else:
            print("The ranks of the tree nodes are inconsistent!\n")

    # if not self.isRankConsistent():
    # print("The ranks of the tree nodes are inconsistent!")

    """Checks if the tree is an AVL

    @rtype: boolean 
    @returns: True if the tree is an AVL tree
    """

    def isAVL(self):
        return self.isAVLRec(self.getRoot())

    """Checks if the subtree is an AVL
    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if the subtree is an AVL tree
    """

    def isAVLRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            return True
        # Check abs(balance factor) <= 1
        bf = (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(x)
        if bf > 1 or bf < -1:
            return False
        # Recursive calls
        return self.isAVLRec(x.getLeft()) and self.isAVLRec(x.getRight())

    """Checks if sizes of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if sizes of the nodes in the tree are consistent
    """

    def isSizeConsistent(self):
        return self.isSizeConsistentRec(self.getRoot())

    """Checks if sizes of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if sizes of the nodes in the subtree are consistent
    """

    def isSizeConsistentRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            if x.size == 0:
                return True
            else:
                return False
        # Size of x should be x.left.size + x.right.size + 1
        if x.size != (x.getLeft().size + x.getRight().size + 1):
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if heights of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if heights of the nodes in the tree are consistent
    """

    def isHeightConsistent(self):
        return self.isHeightConsistentRec(self.getRoot())

    """Checks if heights of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if heights of the nodes in the subtree are consistent
    """

    def isHeightConsistentRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            return True
        # Height of x should be maximum of children heights + 1
        if x.getHeight() != max(x.getLeft().getHeight(), x.getRight().getHeight()) + 1:
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if the ranks of the nodes in the tree are consistent

    @returns: True if the ranks of the nodes in the tree are consistent
    """

    def isRankConsistent(self):
        root = self.getRoot()
        for i in range(1, root.size):
            if i != self.rank(self.retrieve_rec(i + 1)):
                return False
        # nodesList = self.nodes()
        # for node in nodesList:
        # if node != self.retrieve_rec(self.search(node)):
        # return False
        return True

    """Returns a list of the nodes in the tree sorted by index in O(n)

    @rtype: list
    @returns: A list of the nodes in the tree sorted by index
    """

    def nodes(self):
        lst = []
        self.nodesInOrder(self.getRoot(), lst)
        return lst

    """Adds the nodes in the subtree to the list
     following an in-order traversal in O(n)

    @type x: AVLNode
    @type lst: list
    @param x: The root of the subtree
    @param lst: The list
    """

    def nodesInOrder(self, x, lst, pr=False):
        if not x.isRealNode():
            return
        self.nodesInOrder(x.getLeft(), lst)
        lst.append(x)
        self.nodesInOrder(x.getRight(), lst)

    def checkInsert(self, lst, name):
        passTest = True
        print("Check insert test (input=#", name, "#):   *(50 inserts)")
        if self.size != len(lst):
            passTest = False
            print("Size of the tree #", name, "# != len(lst) --> ", self.size, "!=", len(lst))
        for i in range(50):
            index = random.randint(0, self.getSize())
            val = random.randint(65, 122)
            self.insert(index, val)
            lst.insert(index, val)
            if self.size != len(lst):
                passTest = False
                print("Iter num. ", i + 1, ": Size of the tree #", name, "# != len(lst) --> ", self.size, "!=",
                      len(lst))
        self.check(name)
        for i in range(self.size):
            if self.retrieve(i) != lst[i]:
                passTest = False
                print("AVLtree[", i, "] != lst[", i, "] --> # ", self.retrieve(i), " != ", lst[i])
        if passTest:
            print("Good! AVL tree #", name, "# passed the test")

    def checkDelete(self, lst, name):
        passTest = True
        print("Check insert test (input=#", name, "#):   *(50 inserts)")
        if self.size != len(lst):
            passTest = False
            print("Size of the tree #", name, "# != len(lst) --> ", self.size, "!=", len(lst))
        delNum = random.randint(1, self.getSize())
        for i in range(delNum):
            index = random.randint(0, self.getSize() - 1)
            avlElem = self.retrieve()
            lstElem = lst[index]
            self.delete(index)
            del lst[index]
            # CHECK IF LST==AVL
            for j in range(self.getSize()):
                rIndex = random.randint(0, self.getSize() - 1)
                if self.retrieve(rIndex) != lst[rIndex]:
                    passTest = False
                    print("AVLtree[", rIndex, "] != lst[", rIndex, "] --> # ", self.retrieve(rIndex), " != ",
                          lst[rIndex])
                    print("Criminal deletion --> AVL[", index, "]:", avlElem, "|| lst[", index, "]:", lstElem)

        if passTest:
            print("Good! AVL tree #", name, "# passed the test")

    def printTree(self, name=""):
        print("AVL tree: ", name)
        tLst = printree(self)
        for n in tLst:
            print(n)

    """ Lists generator
    :rType: (AVL tree , Array) 
    :return: AVL tree list , Array list
    """


def listsGenerator():
    t = AVLTreeList()
    lst = []
    chooseLen = random.randint(0, 23)
    for i in range(chooseLen):
        chooseType = random.randint(1, 3)  # 3-> string , 2 -> int, 1 -> char
        if chooseType == 3:
            lengthStr = random.randint(2, 7)
            val = strGenerator(lengthStr)
        elif chooseType == 2:
            val = str(random.randint(0, 100))
        else:
            val = chr(random.randint(65, 96))
        index = random.randint(0, i)
        t.insert(index, val)
        lst.insert(index, val)

    return t, lst


def strGenerator(len):
    res = [chr(random.randint(65, 96)) for i in range(len)]
    return "".join(res)


def arrayPrinter(t):
    lt = t.nodes()
    lb = []
    lv = []
    for k in range(len(lt)):
        e = []
        d = []
        if not isinstance(lt[k], AVLNode):
            print("None node in lt[", k, "] -> should be a vr!")
            lv.append("None")
            d.append("None -->")
        else:
            if lt[k].value is None:
                lv.append("VR")
                d.append("VR -->")
            else:
                lv.append(lt[k].value)
                d.append(lt[k].value + " -->")

        if not isinstance(lt[k].left, AVLNode):
            print("None node in lt[", k, "].Left -> should be a vr!")
            e.append("N")
        else:
            if lt[k].left is None:
                e.append("VR")
            else:
                e.append(lt[k].left.value)

        if not isinstance(lt[k].parent, AVLNode) and lt[k] is not t.root:
            print("None node in lt[", k, "].parent -> not root, so it is a mistake")
        else:
            if lt[k].parent is None:
                e.append("None of root")
            else:
                e.append(lt[k].parent.value)

        if not isinstance(lt[k].right, AVLNode):
            print("None node in lt[", k, "].Right -> should be a vr!")
        else:
            if lt[k].right is None:
                e.append("VR")
            else:
                e.append(lt[k].right.value)
        d.append(e)
        lb.append(d)
    if len(lt) != len(lb):
        print("sizes not good")
    print("\nList of values in order: ", lv)
    print("List of branches in order: ", lb, "\n")

    def check1_i_d(self, l1):
        for i in range(8):
            print("### TEST " + chr(i + 65) + " ###\n", l1)
            # t1.printTree("Del " + chr(i + 65) + "[size=" + str(t1.size) + "]")
            # arrayPrinter(t1)
            val = t1.retrieve(i)
            print("\n", chr(i + 65) + ".) Delete value #", val, "#")
            t1.delete(i)
            del l1[i]
            # print("After delete(", val, "):\n", l1)
            t1.check("After delete(" + val + "):\n")
            t1.printTree("AFTER DEL [" + chr(i + 65) + "]")
            # arrayPrinter(t1)
            s = True
            for j in range(9):
                if t1.retrieve(j) != l1[j]:
                    s = False
                    print("failed -> t1.retrieve(", j, ") != l1[", j, "] --> ", t1.retrieve(j), " != ", l1[j], "", )
            t1.insert(i, val)
            l1.insert(i, val)
            if s:
                print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("$$$$$$$$   ", chr(i + 65) + " IS A SUCCESS TEST !!!   $$$$$$$$")
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("\n")
        t1.printTree("Initial tree")
        print(l1)

def main():
    t1, t2, t3 = AVLTreeList(), AVLTreeList(), AVLTreeList()
    l1 = [str(i) for i in range(10)]  # [0, 1, 2, 3, ... , 9]
    l2 = [str(i) for i in range(0, 20, 2)]  # [0, 2, 4, 6, ... , 18]
    l3 = [chr(i) for i in range(65, 91)]  # ['a', 'b', 'c', ... , 'z']
    i1 = [t1.insert(i, str(i)) for i in range(10)]  # [0, 1, 2, 3, ... , 9]
    i2 = [t2.insert(i / 2, str(i)) for i in range(0, 20, 2)]  # [0, 2, 4, 6, ... , 18]
    i3 = [t3.insert(i - 65, chr(i)) for i in range(65, 91)]  # ['a', 'b', 'c', ... , 'z']
    t1.check1_i_d(l1)

#################################################################################################
#################################################################################################

                                  ### PRINTER FUNCTION ###
def printree(t, bykey=False):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    return trepr(t, t.getRoot(), bykey)


def trepr(t, node, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if not isinstance(node, AVLNode):
        return ["None"]

    if not node.isRealNode():  # You might want to change this, depending on your implementation
        return ["#"]  # Hashtag marks a virtual node

    thistr = str(node.getValue())

    return conc(trepr(t, node.getLeft(), bykey), thistr, trepr(t, node.getRight(), bykey))


def conc(left, root, right):
    """Return a concatenation of textual representations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i


if __name__ == "__main__":
    main()
