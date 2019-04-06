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


funcMap =	{
  "and": andFunc,
  "or": orFunc,
  "xor": xorFunc,
  "not": notFunc
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

def naive_solution(input):
    tree , varSet = generateTree(input)
    f = booleanFunction(tree, varSet)
    solutions = [] 
    naive_helper(f, [], 0, solutions, len(varSet.keys()))
    return solutions

def naive_helper(f, curr_list, curr_index, solutions, max_length):
    if curr_index == max_length:
        if f(curr_list):
            solutions.append(curr_list)
    else:
        naive_helper(f, curr_list + [True], curr_index + 1, solutions, max_length)
        naive_helper(f, curr_list + [False], curr_index + 1, solutions, max_length)

def markRequiredTrue:


tree , varSet = generateTree("(! A) || B")
f = booleanFunction(tree, varSet)
print (f([False, True]))

print (naive_solution("(! A)  B"))