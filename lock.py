# encoding: utf-8
"""
    How to setup cache:
    
    # with django
    import lock
    from django.core.cache import cache
    lock.CACHE = cache
    
    # with memcached
    import lock
    import memcache
    lock.CACHE = memcache.Client(['127.0.0.1:1122'])
"""


try:
    from django.core.cache import cache as CACHE
except ImportError:
    CACHE=None

import time

class DistributedLock(object):
    
    LOCK_VALUE=1
    
    def __init__(self, lock_name, timeout):
        self.lock_name = "lock:%s" % lock_name
        self.timeout = timeout
        self._locked = False
        
    def is_locked(self):
        if self._locked:
            value = CACHE.get(self.lock_name)
            if value:
                if time.time() < value:
                    return True
                else:
                    self._locked = False
        return False
        
    def try_lock(self, retry=False):
        while True:
            try:
                self.ensure_lock()
                return True
            except LockNotAcquiredError:
                if not retry:
                    return False
                time.sleep(1)
        
    def release(self):
        if self.is_locked():
            CACHE.delete(self.lock_name)
            self._locked = False
            return True
        raise LockNotAcquiredError()
        
    def ensure_lock(self):
        if self.is_locked():
            return True

        lock_value = time.time() + self.timeout
        # tenta bloquear e retorna status
        chave_criada = CACHE.add(self.lock_name, lock_value, self.timeout)
        if not chave_criada:
            raise LockNotAcquiredError()
            
        self._locked = True

    def __enter__(self):
        self.try_lock(retry=True)
        
    def __exit__(self, type, value, traceback):
        self.release()
        
    # def wait(self, max_timeout):
#         


class LockNotAcquiredError(Exception):
    pass


def serializable(lock_name, timeout):
    lock = DistributedLock(lock_name, timeout)
    
    def prepare_func(f):
        def wrapped(*args, **kargs):
            with lock:
                f(*args, **kargs)
        return wrapped
    return prepare_func


#===========================================================


@serializable('meu_lock', 10)
def teste_bloqueado():
    print "executando com semaforo"
    raise "ssds"
    time.sleep(5)
    print "fim execução"

if '__name__' == '__main__':
    
    print "chamando"
    teste_bloqueado()
    print "terminei de chamar"
    
    

