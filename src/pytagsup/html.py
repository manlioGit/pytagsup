"""
Void html elements. W3C [reference](https://www.w3.org/TR/2011/WD-html-markup-20110405/syntax.html#syntax-elements)

Example:
  from pytagsup.html import *

  class A:
    def xxx(self):
      return img(attr({'src':"xxx"})).render()

  >> A().xxx()
  => <img src='xxx'/>

NonVoid html elements.

Example:
  from pytagsup.html import *

  class A:
    def xxx(self):
      return div(attr({'class':"fa fa-up"})).render()

   >> A().xxx()
   => <div class='fa fa-up'></div>
"""
from functools import partial
from importlib import import_module
from pytagsup.tags import Group, NonVoid, Text, Void
from pytagsup.attribute import Attribute

def html5(*renderable):
  return Group(Text("<!DOCTYPE html>"), NonVoid("html", *renderable))

def attr(attributes = {}):
  return Attribute(attributes)

def text(string):
  return Text(string)

def group(*tags):
  return Group(*tags)

mod = import_module(__name__)
for m in [
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
    'input','keygen', 'link', 'meta','param', 'source', 'track', 'wbr'
  ]:
  setattr(mod, m, partial(lambda n, a = Attribute(): Void(n, a), m))

for m in [
    'a', 'abbr', 'address', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo', 'blockquote', 'body', 'button',
    'canvas', 'caption', 'cite', 'code', 'colgroup', 'data', 'datalist', 'dd', 'del', 'dfn', 'div', 'dl',
    'dt', 'em', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'head', 'header', 'i', 'iframe', 'ins', 'kbd', 'label', 'legend', 'li', 'main', 'map',
    'mark', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'pre', 'progress',
    'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'span', 'strong',
    'style', 'sub', 'sup', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title',
    'tr', 'u', 'ul', 'var', 'video'
  ]:
  setattr(mod, m, partial(lambda n, a = Attribute(), *renders: NonVoid(n, a, *renders), m))