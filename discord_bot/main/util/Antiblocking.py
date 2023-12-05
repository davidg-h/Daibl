import typing # For typehinting 
import functools
import asyncio

async def run_blocking(blocking_func: typing.Callable, client, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)

def run_async_in_thread(callback, arg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(callback(arg))
    loop.close()