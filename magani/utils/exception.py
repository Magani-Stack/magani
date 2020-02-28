d = {
    "no": "yes"
}


class CustomError:

    def __init__(self, fun):
        self.fun = fun

    def __call__(self, *args, **kwargs):
        try:
            return self.fun(*args, **kwargs)
        except Exception as e:
            print(e)
            raise Exception(d.get(str(e)))


@CustomError
def a():
    raise Exception("no")
