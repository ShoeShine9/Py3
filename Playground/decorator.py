def add_ints(a, b):
    return a + b


def test(func):

    def new_func(*args, **kwargs):
        print('starting:', func.__name__)
        print('positional args:', args)
        print('keyword args:', kwargs)
        result = func(*args, **kwargs)
        print('result:', result)
    return new_func

tested_add = test(add_ints)

tested_add(5, 3)