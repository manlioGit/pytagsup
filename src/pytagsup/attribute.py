from functools import reduce
from itertools import chain

class Attribute:

  def __init__(self, attributes = {}):
    self._attributes = Attribute._init(attributes)

  def add(self, other):
    return self._iterate(other, self._add)
  
  def remove(self, other):
    if isinstance(other, str):
      self._attributes.pop(other)

    return self._iterate(other, self._remove)
  
  def render(self):
    return reduce(
      lambda s, k: s + f" {k}='{' '.join(self._attributes[k])}'",
      self._attributes,
      ""
    )
  
  def __eq__(self, other: object):
    if isinstance(other, Attribute):
      return (
        sorted(self._attributes.keys()) == sorted(other._attributes.keys()) and
        sorted(chain(*(self._attributes.values()))) == sorted(chain(*(other._attributes.values())))
      )
    return False

  def _init(obj):
    if isinstance(obj, dict):
      return {
        k: str(v).replace("'", "&#x27;").split() for k,v in filter(lambda x: (x[0] or '').strip() and x[1] != None, obj.items())
      }
    if isinstance(obj, Attribute):
      return obj._attributes

    return {}

  def _add(self, k, e):
    if k not in self._attributes: self._attributes[k] = [] 
    if e not in self._attributes[k]: 
      self._attributes[k].append(e)

  def _remove(self, k, e):
    if e in self._attributes.get(k, []): 
      self._attributes[k].remove(e)

  def _iterate(self, other, f):
    for k,v in Attribute._init(other).items():
      for e in v:
        f(k,e)

    return self