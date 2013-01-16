import distributedlock

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
    
    def test_ensure_will_lock_will_call_function_and_release(self, lock):
        called = False
        with distributedlock.distributedlock('ola', lock=lock):
            called = True
        assert called
        assert lock.acquired_called == 1
        assert lock.release_called == 1

    def test_after_raise_exception_release_is_called(self, lock):
        myError = RuntimeError("myError")
        
        try:
            with distributedlock.distributedlock('ola2', lock=lock):
                raise myError
                
            assert False, "Never run"
        except Exception, e:
            assert e is myError
            assert lock.acquired_called == 1
            assert lock.release_called == 1
            
    def test_lock_not_acquired_and_noblocking_raise_exception(self, lock, monkeypatch):
        # no lock
        def never_acquire(blocking):
            assert not blocking
            return False
            
        monkeypatch.setattr(lock, 'acquire', never_acquire)

        try:
            with distributedlock.distributedlock('ola', lock=lock, blocking=False):
                raise RuntimeError("There is a problem!!!")
            assert False
        except distributedlock.LockNotAcquiredError:
            pass
            
    def test_if_block_throws_an_exception_it_will_not_be_captured(self, lock, monkeypatch):
        myerror = RuntimeError('myerror2')
        def raise_exception(blocking):
            raise myerror
        
        monkeypatch.setattr(lock, 'acquire', raise_exception)

        try:
            with distributedlock.distributedlock('ola', lock=lock):
                assert False, 'Never can run'
            assert False, 'Never can run'
        except Exception, e:
            assert e is myerror

