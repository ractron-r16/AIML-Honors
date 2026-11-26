from functools import wraps


def output_decorator(label):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            formatted_args = ", ".join(str(item) for item in args)
            if kwargs:
                extra = ", ".join(f"{k}={v}" for k, v in kwargs.items())
                display_input = f"{formatted_args}, {extra}" if formatted_args else extra
            else:
                display_input = formatted_args

            print("=" * 26)
            print(f"# {label}")
            print(f"# input: {display_input}")

            result = func(*args, **kwargs)

            print(f"# output: {result}")
            print("=" * 26)
            return result

        return wrapper

    return decorator


@output_decorator("Adding")
def add(a, b):
    return a + b


@output_decorator("Multiplication")
def multiply(a, b):
    return a * b


if __name__ == "__main__":
    add(4, 3)
    add(15, 25)
    multiply(6, 8)
