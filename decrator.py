from functools import wraps
def deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("before myfunc() called.")
        result = func(*args, **kwargs)
        print("after myfunc() called.")
        return result
    return wrapper

@deco
def myfunc(a, b):
    print("myfunc(%s, %s) called." % (a, b))
    return a + b

print(myfunc(1, 2))
print("name: %s, doc: %s" % (myfunc.__name__, myfunc.__doc__))
#myfunc()
