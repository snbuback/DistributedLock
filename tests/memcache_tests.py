#encoding: utf-8
import distributedlock
from distributedlock.memcachedlock import MemcachedLock
import time

# added = self.client.add(self.key, self.instance_id, self.timeout)
# value = self.client.get(self.key)
# self.client.delete(self.key)

def create_mlock(key, client):
    return MemcachedLock(key, client)
    
    
class TestMemcacheLock(object):
    
    def test_when_memcacheclient_added_method_returns_0_raise_runtimeerror(self):
        class MClient(object):
            def add(self, key, val, timeout):
                return 0

        try:
            lock = create_mlock('ola', MClient())
            with distributedlock.distributedlock('ola', lock=lock):
                assert False
            assert False
        
        except RuntimeError:
            pass


    def test_when_memcacheclient_added_method_returns_False_and_no_blocking_raise_LockNotAcquiredError(self):
        class MClient(object):
            def add(self, key, val, timeout):
                return False

        try:
            lock = create_mlock('ola', MClient())
            with distributedlock.distributedlock('ola', lock=lock, blocking=False):
                assert False
            assert False

        except distributedlock.LockNotAcquiredError:
            pass


    def test_when_memcacheclient_added_method_returns_False_and_blocking_wait_forever(self, monkeypatch):
        self.counter = 3

        class MClient(object):
            def add(selfclient, key, val, timeout):
                selfclient.val = val
                return self.counter == 0
                
            def get(self, key):
                return self.val
                
            def delete(self, key):
                pass

        def sleep(i):
            self.counter -= 1

        monkeypatch.setattr(time, 'sleep', sleep)
        lock = create_mlock('ola', MClient())
        called = False
        with distributedlock.distributedlock('ola', lock=lock, blocking=True):
            called = True

        assert called






