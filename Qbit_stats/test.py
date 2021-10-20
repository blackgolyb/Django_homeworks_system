class BaseView(object):
    """docstring for ."""

    def some_dec(func):
        def wrap(self, *args):
            print(args[0])
            if args[0]:
                return func(self, *args)
            return None
        return wrap

    @some_dec
    def get(self, some_args):
        print(123)

class MyView(BaseView):
    def get(self, some_args):
        print('response')


BV = BaseView()
BV.get(False)
MV = MyView()
MV.get(False)
