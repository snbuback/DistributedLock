# encoding: utf-8
from contextlib import contextmanager
import threading
from distributed_lock.memcachedlock import MemcachedLock
try:
    from django.core.cache import cache as CACHE
except ImportError:
    CACHE=None

DEBUG = False
DEFAULT_TIMEOUT=60
DEFAULT_BLOCKING=False
DEFAULT_MEMCACHED_CLIENT=None

def _debug(msg):
    if DEBUG:
        print "LOCK:", msg

class LockNotAcquiredError(Exception):
    pass

@contextmanager
def syncronized_block(key, lock=None, blocking=None):
    # setup default values
    blocking = blocking or DEFAULT_BLOCKING
    
    if not lock:
        lock = MemcachedLock(key, DEFAULT_MEMCACHED_CLIENT, DEFAULT_TIMEOUT)
    
    if lock.acquire(blocking):
        _debug("locking with key %s" % key)
        try:
            yield lock
        finally:
            _debug("releasing lock %s" % key)
            lock.release()
    else:
        raise LockNotAcquiredError()


def syncronized(lock=None, blocking=None):
    
    def prepare_func(f):
        def wrapped(*args, **kargs):
            # FIXME Ajuste chave
            with syncronized_block("ola", lock, blocking):
                f(*args, **kargs)
        return wrapped
    return prepare_func

    

