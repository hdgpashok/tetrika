def strict(func):
    def wrapper(a, b):
        type_a = func.__annotations__.get('a')
        type_b = func.__annotations__.get('b')

        if not (isinstance(a, type_a) and isinstance(b, type_b)):
            raise TypeError

        return func(a, b)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b



print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
