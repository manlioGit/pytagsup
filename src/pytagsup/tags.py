from functools import reduce
from itertools import filterfalse
from pytagsup.attribute import Attribute

class Text:

  def __init__(self, text):
    self._text = text

  def render(self):
    return self._text

  def __eq__(self, other):
    return self._text == other._text if isinstance(other, Text) else False


class Group:

  def __init__(self, *tags):
    self._tags = list(tags)

  def render(self):
    return ''.join(map(lambda t: t.render(), self._tags))
  
  def add(self, tag):
    self._tags.append(tag)
    return self

  def __eq__(self, other):
    return self._tags == other._tags if isinstance(other, Group) else False


class Void:

  def __init__(self, name, attribute = Attribute()):
    self._name = name
    self._attribute = attribute

  def render(self):
    return f"<{self._name}{self._attribute.render()}/>"

  def __eq__(self, other):
    if isinstance(other, Void):
      return self._name == other._name and self._attribute == other._attribute
    return False
  
  
class NonVoid:

  def __init__(self, name, *renders):
    self._name = name
    self._attribute = next((r for r in renders if isinstance(r, Attribute)), Attribute())
    self._children =  list(filterfalse(lambda r: isinstance(r, Attribute), renders))

  def render(self):
    return reduce(
      lambda m, t: m + t.render(),self._children,f"<{self._name}{self._attribute.render()}>"
    ) + f"</{self._name}>"
  
  def add(self, tag):
    self._children.append(tag)
    return self

  def __eq__(self, other):
    return (
      self._name == other._name and 
      self._attribute == other._attribute and
      self._children == other._children
    )