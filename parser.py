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
				| expr "^^" expr -> xor
				| expr "==" expr -> eq
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


def gateCount(tree):
    if isinstance(tree, varNode):
        return 0
    count = 1
    for child in tree.operands:
        count += gateCount(child)
    return count



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
    change = False
    if isinstance(root, opNode):
        for child in root.operands:
            val = collapseTree(child)
            if val:
                change = True
        canCollapse = True
        allVar = True
        for child in root.operands:
            canCollapse =  canCollapse and (isinstance(child, varNode) or (child.op == root.op and root.op != 'not' and root.op != 'nop'))
            allVar = allVar and isinstance(child, varNode)
        if canCollapse and not allVar:
            change = True
            newOperands = []
            for child in root.operands:
                if isinstance(child, varNode):
                    newOperands.append(child)
                else:
                    newOperands += child.operands
            root.operands = newOperands
    return change
def deMorgan(tree):
    change = False
    if isinstance(tree, opNode):
        if(tree.op == 'not'):
            if isinstance(tree.operands[0], opNode):
                if tree.operands[0].op == 'xor':
                    tree.op = 'nop'
                    tree.operands[0].op = 'eq'
                    change = True
                elif tree.operands[0].op == 'eq':
                    tree.op = 'nop'
                    tree.operands[0].op = 'xor'
                    change = True
                elif tree.operands[0].op == 'and':
                    tree.op = 'nop'
                    tree.operands[0].op = 'or'
                    change = True
                    deMorganHelper(tree.operands[0])
                elif tree.operands[0].op == 'or':
                    tree.op = 'nop'
                    tree.operands[0].op = 'and'
                    change = True
                    deMorganHelper(tree.operands[0])
        for child in tree.operands:
            val = deMorgan(child)
            if val:
                change = True
    return change                          


def deMorganHelper(tree):
    newOperands = list()
    for child in tree.operands:
        notNode = opNode('not')
        notNode.operands.append(child)
        newOperands.append(notNode)
    tree.operands = newOperands


def notCondense(tree):
    change = False
    if isinstance(tree, opNode):
        if(tree.op == 'not'):
            if isinstance(tree.operands[0], opNode):
                if(tree.operands[0].op == 'not'):
                    tree.op = 'nop'
                    change = True
                    tree.operands[0].op = 'nop'  
        for child in tree.operands:
            val = notCondense(child) 
            if val:
                change = True 
    return change


def nopRemoval(tree):
    if isinstance(tree, opNode) and tree.op =='nop':
        return (tree.operands[0] , True)
    if isinstance(tree, varNode):
        return (tree , False)
    change = False
    newOperands = list()
    for child in tree.operands:
        newTree, val = nopRemoval(child)
        if val:
            change = True
        newOperands.append(newTree)
    tree.operands = newOperands
    return (tree , change)

def generateTree(input):
    varSet = {}
    tree = createBoolTree(getParsedTree(input), varSet)
    running = True
    while running:
        running = False
        val = collapseTree(tree)
        running = running or val
        val = deMorgan(tree)
        running = running or val
        val = notCondense(tree)
        running = running or val
        tree , val = nopRemoval(tree)
        running = running or val
    return (tree, varSet)



tree , varSet = generateTree("! ((! A) || (! B))")
#collapseTree(tree)
#print (tree.operands)
#printBoolTree(tree)
#print (varSet)

#print (tree.data)

#print (tree.children[1].children[0].children[0].value)

#for node in tree.children:
#	print (node)