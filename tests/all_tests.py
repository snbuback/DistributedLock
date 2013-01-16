import time
import sys
import os
import memcache

# add parent dir to sys.path
lib_dir = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(lib_dir)

# configure logging for tests
import logging
logging.basicConfig()

import distributedlock
from distributedlock.memcachedlock import MemcachedLock

distributedlock.DEFAULT_MEMCACHED_CLIENT = memcache.Client(['127.0.0.1:11211'])

class TestError(Exception):
    """ Raised only in test """
    pass

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


class TestDistributedLock(object):
    
    def test_ensure_lock_call_and_release(self, lock):
        called = False
        with distributedlock.distributedlock('ola', lock=lock):
            called = True
        assert called
        assert lock.acquired_called == 1
        assert lock.release_called == 1

    def test_after_raise_exception_release_is_called(self, lock):
        myError = object()
        try:
            with distributedlock.distributedlock('ola2', lock=lock):
                raise RuntimeError(myError)
                
            raise "Ops... never can be here!!!"
        except Exception, e:
            assert type(e) == RuntimeError
            assert e.message is myError
            assert lock.acquired_called == 1
            assert lock.release_called == 1
            
    def test_lock_not_acquired_raise_exception(self, lock):
        # no lock
        lock.acquire = lambda blocking: False

        try:
            with distributedlock.distributedlock('ola', lock=lock):
                raise RuntimeError("There is a problem!!!")
            raise RuntimeError('Bug')
        except distributedlock.LockNotAcquiredError:
            pass
            
    def test_lock_raise_exception_will_raise_exception(self, lock):
        # no lock
        def raise_exception(block):
            raise TestError()
        
        lock.acquire = raise_exception

        try:
            with distributedlock.distributedlock('ola', lock=lock):
                raise RuntimeError("There is a problem!!!")
            raise RuntimeError('Bug')
        except TestError:
            pass

# class TestMemcacheLock(object):
#     
#     def test_when_added_returns_0_raise_runtimeerror(self, mlock):
#         with distributedlock.distributedlock('ola', lock=lock):
#             time.sleep(10)
#             print "OIIIII"
#         print "OLA"
# 



@distributedlock.distributedlock()
def hello_world(id, name):
    print 'Executando'
    time.sleep(1)
    print 'Fim execução'


class TestDecoratorUsage(object):
    def test_decorator_usage(self):
        hello_world(5, 'rsrs')

