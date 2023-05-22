class Pool:

    def __init__(self, slice_size, class_ref, arg):
        self.__slice = slice_size
        self.__pool = [class_ref(arg) for _ in range(self.__slice)]

    def acquire(self):
        if len(self.__pool) > 0:
            pool_object = self.__pool.pop()
            pool_object.reset()
            return pool_object

    def release(self, pool_object):
        self.__pool.append(pool_object)
