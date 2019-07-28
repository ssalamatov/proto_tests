# -*- coding: utf-8 -*-

import os
import time
import tempfile


def caught(f):
    def _caught(args, **kwargs):
        try:
            f(args, **kwargs)
        except BaseException as e:
            print(e)
    return _caught


def log(state):
    def _log(f):
        def __log(args, **kwargs):
            print('test', ':', state)
            f(args, **kwargs)
        return __log
    return _log


class TestException(Exception):
    msg = 'something is wrong'

    def __str__(self):
        return '%s' % self.msg


class Test:

    tc_id = None
    name = None

    @log('prep')
    def prep(self):
        pass

    @log('run')
    def run(self):
        pass

    @log('clean_up')
    def clean_up(self):
        pass

    @caught
    def execute(self):
        self.prep()
        self.run()
        self.clean_up()

    def __str__(self):
        return '%s' % self.tc_id


class Test1(Test):

    def prep(self):
        super().prep()
        if not int(time.time()) % 2 == 0:
            # cancel task
            raise TestException()

    def run(self):
        super().run()
        print(os.listdir('.'))

    def clean_up(self):
        super().clean_up()


class Test2(Test):

    path = None

    def run(self):
        fd, self.path = tempfile.mkstemp(suffix='', prefix='test', dir=os.path.join('/', 'tmp'))
        try:
            f = open(self.path, 'wb')
            f.write(os.urandom(64 * 1024))
        finally:
            os.close(fd)

    def clean_up(self):

        if self.path:
            os.remove(self.path)


if __name__ == '__main__':

    for cls in (Test1, Test2,):
        cls().execute()
