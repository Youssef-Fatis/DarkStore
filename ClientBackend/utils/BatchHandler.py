import asyncio
from typing import Generic, TypeVar, Optional, List, Callable, Awaitable

T = TypeVar("T")
R = TypeVar("R")


class Iterator(Generic[T]):
    def next(self) -> None:
        raise NotImplementedError

    def current(self) -> T:
        raise NotImplementedError

    def is_end(self) -> bool:
        raise NotImplementedError


class ArrayIterator(Iterator[T]):
    def __init__(self, array: List[T]):
        self.params = array
        self.pointer = 0

    def next(self) -> None:
        self.pointer += 1

    def current(self) -> T:
        return self.params[self.pointer]

    def is_end(self) -> bool:
        return self.pointer >= len(self.params)


class IncrementIterator(Iterator[int]):
    def __init__(self, increment: int, start: int, end: Optional[int] = None):
        self.increment = increment
        self.start = start
        self.end = end
        self.position = start

    def next(self) -> None:
        self.position += self.increment

    def current(self) -> int:
        return self.position

    def is_end(self) -> bool:
        return self.end is not None and self.position > self.end


async def batch_request_handler(
    batch_size: int,
    iterator: Iterator[T],
    fetching_func: Callable[[T], Awaitable[R]],
    breaking_func: Optional[Callable[[R], bool]] = None
) -> List[R]:
    result: List[R] = []
    stop = False

    while not iterator.is_end() and not stop:
        batch_promises = []

        for _ in range(batch_size):
            if iterator.is_end():
                break
            batch_promises.append(fetching_func(iterator.current()))
            iterator.next()

        responses = await asyncio.gather(*batch_promises)

        for response in responses:
            if breaking_func and breaking_func(response):
                stop = True
            result.append(response)

    if breaking_func:
        return [response for response in result if not breaking_func(response)]
    return result
