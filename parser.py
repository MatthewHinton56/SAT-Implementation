from lark import Lark
from queue import *


l = Lark('''?expr: expr "&&" expr -> and
				| expr "||" expr -> or
				| expr "^" expr -> xor
				| "!" expr -> not
                | CNAME -> variable
				| "(" expr ")"

            %import common.CNAME   // imports from terminal library
            %ignore " "           // Disregard spaces in text
         ''', start='expr')


def getParser():
    return  Lark('''?expr: expr "&&" expr -> and
				| expr "||" expr -> or
				| expr "^" expr -> xor
				| "!" expr -> not
                | CNAME -> variable
				| "(" expr ")"

            %import common.CNAME   // imports from terminal library
            %ignore " "           // Disregard spaces in text
         ''', start='expr')   


class opNode:
    def __init__(self, op):
        self.op = op
        self.operands = list()
        self.mustTrue = False
        self.mustFalse = False
    def __str__(self):
        return self.op 


class varNode:
    def __init__(self, name):
        self.name = name
        self.mustTrue = False
        self.mustFalse = False
    
    def __str__(self):
        return self.name



def printBoolTree(root):
    q = Queue()
    q.put((None, root))
    while not q.empty():
        p , f = q.get()
        print (str(p) + str(f))
        if isinstance(f, opNode):
            for child in f.operands:
                q.put((f, child))


def getParsedTree(input):
    l = getParser()
    tree = l.parse(input)
    from lark.tree import pydot__tree_to_png    # Just a neat utility function
    pydot__tree_to_png(tree, "ex.png")
    return tree

def createVariableNode(node, varSet):
    var = str(node.children[0].value)
    if var not in varSet:
        varSet[var] = len(varSet)
    return varNode(var)


def createBoolTree(root, varSet):
    if(root.data == 'variable'):
        return createVariableNode(root, varSet)
    node = opNode(root.data)
    for child in root.children:
        node.operands.append(createBoolTree(child, varSet))
    return node

def collapseTree(root):
    if isinstance(root, opNode):
        for child in root.operands:
            collapseTree(child)
        canCollapse = True
        for child in root.operands:
            canCollapse =  canCollapse and (isinstance(child, varNode) or child.op == root.op)
        if canCollapse:
            newOperands = []
            for child in root.operands:
                if isinstance(child, varNode):
                    newOperands.append(child)
                else:
                    newOperands += child.operands
            root.operands = newOperands
    return root

def generateTree(input):
    varSet = {}
    return (collapseTree(createBoolTree(getParsedTree(input), varSet)), varSet)

#tree , varSet = generateTree("(B && C) && D && (E && D)")
#collapseTree(tree)
#print (tree.operands)
#printBoolTree(tree)
#print (varSet)

#print (tree.data)

#print (tree.children[1].children[0].children[0].value)

#for node in tree.children:
#	print (node)