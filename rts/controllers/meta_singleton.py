"""Singleton for Python."""

from threading import Lock
from weakref import WeakValueDictionary


class MetaSingleton(type):
    """This is a thread-safe implementation of Singleton.

    Returns:
      Thread safe singleton.
    """

    _instances = WeakValueDictionary()
    _lock: Lock = Lock()
    """We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
  """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
