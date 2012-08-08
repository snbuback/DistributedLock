# encoding: utf-8
import time
import uuid
import threading

class MemcachedLock(object):
    """
    Try to do same as threading.Lock, but using Memcached to store lock instance to do a distributed lock
    """

    def __init__(self, key, client, timeout=60):
        self.key = "lock:%s" % key
        self.client = client
        self.timeout = timeout

        # When you use threading.Lock object, instance references acts as ID of the object. In memcached
        # we have a key to identify lock, but to identify which machine/instance/thread has lock is necessary
        # put something in memcached value to identify it. So, each MemcachedLock instance has a random value to 
        # identify who has the lock
        self.instance_id = uuid.uuid1().hex

    def acquire(self, blocking=True):
        while True:
            added = self.client.add(self.key, self.instance_id, self.timeout)
            if added:
                break
            if not blocking and not added:
                return False
            time.sleep(1)
        return True

    def release(self):
        value = self.client.get(self.key)
        if value == self.instance_id:
            # Avoid short timeout, because if key expires, after GET, and another lock occurs, memcached remove
            # below can delete another lock! There is no way to solve this in memcached
            self.client.delete(self.key)
        else:
            raise threading.ThreadError("I've no lock to release")



