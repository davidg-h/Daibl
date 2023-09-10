import asyncio
import functools
import os
import typing

class add_path():
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.old_path = os.environ['PATH']
        os.environ['PATH'] = self.path + os.pathsep + self.old_path

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ['PATH'] = self.old_path
        
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        wrapped = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, wrapped)
    return wrapper