import time
import sys
import os
import memcache

# add parent dir to sys.path
lib_dir = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(lib_dir)

import distributed_lock
from distributed_lock import syncronized_block, syncronized

distributed_lock.DEFAULT_MEMCACHED_CLIENT = memcache.Client(['127.0.0.1:11211'])

class MockLock(object):
    def __init__(self):
        self.acquired_called = 0
        self.release_called = 0
    
    def acquire(self, blocking):
        self.acquired_called += 1
        return self.acquired_called == 1
        
    def release(self):
        self.release_called += 1


def pytest_funcarg__lock(request):
    return MockLock()


class TestSyncronizedBlock(object):
    
    def test_block_usage(self, lock):
        with syncronized_block('ola', lock=lock):
            pass
        assert lock.acquired_called == 1
        assert lock.release_called == 1

    def test_after_raise_exception_release_is_called(self, lock):
        try:
            with syncronized_block('ola2', lock=lock):
                raise RuntimeError("asasa")
                
            raise "Não deveria ter chegado aqui"
        except Exception, e:
            assert type(e) == RuntimeError
            assert e.message == 'asasa'
            assert lock.acquired_called == 1
            assert lock.release_called == 1


@syncronized()
def hello_world():
    print 'Executando'
    time.sleep(1)
    print 'Fim execução'


class TestDecoratorUsage(object):
    def test_decorator_usage(self):
        hello_world()

