from parser import *


def andFunc(l):
    out = True
    for v in l:
        out = out and v
    return out

def orFunc(l):
    out = False
    for v in l:
        out = out or v
    return out   

def xorFunc(l):
    out = False
    for v in l:
        out = out ^ v
    return out  

def notFunc(v):
    return (not v[0])

def nopFunc(v):
    return (v[0])

def eqFunc(l):
    test = l[0]
    out = True
    for v in l:
        out = out and (test == v)
    return out 


funcMap =	{
  "and": andFunc,
  "or": orFunc,
  "xor": xorFunc,
  "not": notFunc,
  "nop": nopFunc,
  'eq': eqFunc
}


def booleanFunction(tree, var_array):
    if isinstance(tree, varNode):
        variable = var_array[tree.name]
        return lambda test: test[variable]
    funcs = list()
    for node in tree.operands:
        funcs.append(booleanFunction(node, var_array))
    function = funcMap[tree.op]
    def h(test):
        values = list()
        for func in funcs:
            values.append(func(test))
        return function(values)
    return h

naive_count = 0
mark_count = 0

def naive_solution(input):
    global naive_count
    naive_count = 0
    tree , varSet = generateTree(input)
    f = booleanFunction(tree, varSet)
    solutions = [] 
    naive_helper(f, [], 0, solutions, len(varSet.keys()))
    return solutions

def naive_helper(f, curr_list, curr_index, solutions, max_length):
    global naive_count
    naive_count += 1
    if curr_index == max_length:
        if f(curr_list):
            solutions.append(curr_list)
    else:
        naive_helper(f, curr_list + [True], curr_index + 1, solutions, max_length)
        naive_helper(f, curr_list + [False], curr_index + 1, solutions, max_length)


def mark_solution(input):
    global mark_count
    mark_count = 0
    tree , varSet = generateTree(input)
    valid, required = markRequired(tree, varSet)
    if not valid:
        return []
    f = booleanFunction(tree, varSet)
    solutions = [] 
    mark_helper(f, [], 0, solutions, len(varSet.keys()), required)
    return solutions    



def mark_helper(f, curr_list, curr_index, solutions, max_length, required):
    global mark_count
    mark_count += 1
    if curr_index == max_length:
        if f(curr_list):
            solutions.append(curr_list)
    else:
        if curr_index in required:
            mark_helper(f, curr_list + [required[curr_index]], curr_index + 1, solutions, max_length, required)
        else:
            mark_helper(f, curr_list + [True], curr_index + 1, solutions, max_length, required)
            mark_helper(f, curr_list + [False], curr_index + 1, solutions, max_length, required)





#Returns True if possible, can determine if an equation is impossible if variable X must be both True and False
def markRequired(tree, varSet):
    required = {}
    valid = required_helper(tree, required, True, True, varSet)
    return (valid, required)

def required_helper(tree, required, current, and_chain, varSet):
    if and_chain:
        if current:
            tree.mustTrue = True
        else:
            tree.mustFalse = False
        if isinstance(tree, varNode):
            if tree.name in required and current != required[varSet[tree.name]]:
                return False
            required[varSet[tree.name]] = current
    newCurrent = current
    new_and_chain = and_chain
    if isinstance(tree, opNode):
        if tree.op == 'not':
            newCurrent = not newCurrent
        if tree.op == 'xor' or tree.op == 'or':
            new_and_chain = False
        for child in tree.operands:
            required_helper(child, required, newCurrent, new_and_chain, varSet)
    return True


print (naive_solution(" ((! A) || (! B))"))
print (mark_solution(" ((! A) || (! B))"))
print (naive_count)
print (mark_count)