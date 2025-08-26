class List(list):
    def __init__(self, items):
        super().__init__(items)

    def map(self, func):
        if isinstance(func, str):
            func = eval('lambda ' + func.replace('=>', ': ', 1))

        return List([func(item) for item in self])
    
    def first(self):
        return self[0] if self else None
        
if __name__ == '__main__':
    print(List([1,2,3]).map('x => x ** 2'))