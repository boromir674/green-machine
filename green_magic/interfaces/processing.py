# from abc import ABC, abstractmethod
# from typing import Any, Optional



#
# class Handler(ABC):
#     """
#     The Handler interface declares a method for building the chain of handlers.
#     It also declares a method for executing a request.
#     """
#
#     @abstractmethod
#     def set_next(self, handler: Handler) -> Handler:
#         pass
#
#     @abstractmethod
#     def handle(self, request) -> Optional[str]:
#         pass
#
#
# class AbstractHandler(Handler):
#     """
#     The default chaining behavior can be implemented inside a base handler
#     class.
#     """
#
#     _next_handler: Handler = None
#
#     @property
#     def next_handler(self):
#         return self._next_handler
#
#     @next_handler.setter
#     def next_handler(self, next_handler):
#         self._next_handler = next_handler
#
#     def set_next(self, handler: Handler) -> Handler:
#         self._next_handler = handler
#         # Returning a handler from here will let us link handlers in a
#         # convenient way like this:
#         # monkey.set_next(squirrel).set_next(dog)
#         return handler
#
#     @abstractmethod
#     def handle(self, request: Any) -> object:
#         if self._next_handler:
#             return self._next_handler.handle(request)
#         return None
#
#
# """
# All Concrete Handlers either handle a request or pass it to the next handler in the chain.
# """
#
# class DataHandler(AbstractHandler):
#     def handle(self, request: Any) -> object:
#         if request == "Banana":
#             return f"Monkey: I'll eat the {request}"
#         else:
#             return super().handle(request)
#
# class DataframeHandler(AbstractHandler):
#     def handle(self, request: Any) -> str:
#         if request == "Banana":
#             return f"Monkey: I'll eat the {request}"
#         else:
#             return super().handle(request)
#
#
#
