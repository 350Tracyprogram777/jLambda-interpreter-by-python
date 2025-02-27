# 错误处理
def err(msg):
    raise Exception(msg)

# 扩展环境变量
def extend_env(params, args, env):
    # 把参数和参数值组成字典
    e = {p: a for (p, a) in zip(params, args)}
    #返回新的环境变量（字典），其中包含由外部传入的环境变量和参数
    return (e, env)
# 环境变量
env = ({'x': 1, 'y': 2}, None)

# 查找变量的值
def lookup_var(var, env):
    e0 = env

    while e0 != None:
        e, e0 = e0
        if var in e:
            return e[var]

    err(f'未定义变量{var}')

# 设置变量的值
def set_var(var, val, env):
    e0 = env
    # 遍历所有作用域，看看是否有这个变量
    while e0 != None:
        e, e0 = e0
        if var in e:
            e[var] = val
            return   # 找到了直接赋值，就直接返回

    # 没有找到，就在最外层的作用域中设置
    e,_ = env
    e[var] = val

# 计算表达式
def eval(exp,env):
    # 直接返回数字、布尔值、浮点数
    if type(exp) in [int, bool, float]:
        return exp
    
    #返回变量的值
    if type(exp) == str:
        return lookup_var(exp,env)
    
    #为变量赋值
    # ['x','=',3]
    if type(exp) == list and len(exp) == 3 and exp[1] == '=':
        var, _, e = exp
        # 设置变量的值
        set_var(var, val, env)
        # 返回赋值后的值
        return val
    # ['if', cond, e1, e2]
    if type(exp) == list and len(exp) == 4 and exp[0] == 'if':
        _, cond, e1, e2 = exp
        if eval(cond,env):
            return eval(e1,env)
        else:
            return eval(e2,env)

    # [1, '+', 2]
    if type(exp) == list and len(exp) == 3 and exp[1] in ['+', '-', '*', '/', '==', '!=', '>', '>=', '<', '<=']:
        e1, op, e2 = exp

        v1 = eval(e1, env)
        v2 = eval(e2, env)

        if op == '+':
            return v1 + v2
        if op == '-':
            return v1 - v2
        if op == '*':
            return v1 * v2
        if op == '/':
            return v1 / v2
        if op == '==':
            return v1 == v2
        if op == '!=':
            return v1 != v2
        if op == '<':
            return v1 < v2
        if op == '<=':
            return v1 <= v2
        if op == '>':
            return v1 >= v2
        if op == '>=':
            return v1 >= v2

    #['add', '=', ['fun', ['a', 'b'], ['a', '+', 'b']]]
    if type(exp) == list and len(exp) == 3 and exp[0] == 'fun':
        _, params, body = exp
        return ['proc', params, body, env]

    # ['add',[1,2]]
    if type(exp) == list and len(exp) == 2:
        f, args = exp
        proc = eval(f, env)
        if not (type(proc) == list and len(proc) == 4 and proc[0] == 'proc'):
            err(f'非法函数{proc}')

        _, params, body, saved_env = proc

        args = [eval(a, env) for a in args]

        proc_env = extend_env(params, args, saved_env)

        return eval(body, proc_env)

    err(f'非法表达式{exp}')

e1 = ['add', '=', ['fun', ['a', 'b'], ['a', '+', ['b', '+', 'x']]]]
e2 = ['add', [1, 2]]
e3 = ['add', ['x', ['x', '+', 'y']]]