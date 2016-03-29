from threading import Timer

import sched


class abc:
    def __init__(self):
        self.__a = 1
        self.b = 2

    def __a(self):
        return 3

class TestTimer(object):
    def __init__(self):
        self.t = Timer(0.5,self.func)
        self.t.start()

    def func(self):
        print "hello world!"
        self.t = Timer(2,self.func)
        self.t.start()



if __name__ == "__main__":
    t = TestTimer()

    '''
    def hello():
        print "hello, world"
        timer = Timer(3,hello)
        timer.start()

    t = Timer(3.0, hello)
    t.start() # after 30 seconds, "hello, world" will be printed
    '''

