
# from subprocess import call

# from symtable import Function

# from typing import List
# from urllib.request import AbstractDigestAuthHandler

from typing import List
from xmlrpc.client import boolean

class JsList (List):
    def __init__(self, jsLikeList):
      super().__init__(self)
      self.extend(jsLikeList)
    
    def reduce(self, callback, prev = '@@reduce_init'):
      process_is_stop:bool = False
      def force_stop (arg):
        process_is_stop = True
        return arg
      for index in range(len(self)):
        if process_is_stop: break
        item = self[index]
        prev = item if prev == '@@reduce_init' else callback(prev, item, index, self, force_stop)
      return prev
    
    def map(self, callback):
      return self.gen_another_or_not(self.reduce(lambda prev, current, index: [*prev, callback(current)], []))
    
    def filter(self, callback):
      return self.gen_another_or_not(
        self.reduce(lambda prev, current,*rest:([*prev, current] if bool(callback(current)) else prev ) , [])
      )

    def forEach(self, callback):
      return self.reduce(lambda prev,current,index, arr, force_stop: callback(current, index, self, force_stop), self)
    
    def push(self, *args):
      self.append(*args) if len(args) == 1 else self.extend(args)

    def gen_another_or_not (self, target):
      return JsList(target) if type(target) == list else target

    def includes (self, target):
      return self.reduce(lambda prev,current,index,arr,force_stop: (prev and force_stop(prev)) or current == target, False)
    
    def at (self, index: int):
      return None if (index >= 0 and index >= len(self)) or (index < 0 and -index > len(self)) else self.gen_another_or_not(self[index])

    def every(self, callback):
      return self.reduce(lambda prev,current,index,arr, stop: stop(False) if not bool(prev) else callback(current, index), True)
      
    def some(self, callback):
      return self.reduce(lambda prev,current,index, arr, stop: stop(True) if bool(prev) else callback(current, index), False)
    
    def slice(self, start:int, end:int):
      return self.gen_another_or_not(
        self[start:end] if (start and end) else self[start:] if start else self[:]
      )

    @property
    def length(self):
      return len(self)

l2 = JsList([1,2,3,4,5,6,7,8,9])
