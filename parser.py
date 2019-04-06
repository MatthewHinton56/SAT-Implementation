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
    q.put(root)
    while not q.empty():
        f = q.get()
        print (f)
        if isinstance(f, opNode):
            for child in f.operands:
                q.put(child)


def getParsedTree(input):
    l = getParser()
    tree = l.parse(input)
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

def generateTree(input):
    varSet = {}
    return (createBoolTree(getParsedTree(input), varSet), varSet)

tree , varSet = generateTree("A || B")
#print (varSet)

#print (tree.data)

#print (tree.children[1].children[0].children[0].value)

#for node in tree.children:
#	print (node)