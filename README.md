# Pytagsup

Pytagsup is a small XML/HTML construction templating library for Python, inspired by [JavaTags](https://github.com/manlioGit/javatags).

It can renders fragments like:

```python
from pytagsup.html import *

html5(attr({'lang': "en"}),
  head(
    meta(attr({'http-equiv': "Content-Type", 'content': "text/html; charset=UTF-8"})),
    title(text("title")),
    link(attr({'href': "xxx.css", 'rel': "stylesheet"}))
  )
).render()
```

in html:

```html
<!DOCTYPE html>
<html lang='en'>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
    <title>title</title>
    <link href='xxx.css' rel='stylesheet'/>
 </head>
</html>
```

## Installation

Add this line to your application's Gemfile:

```python
pip install pytagsup
```

## Online converter

To convert html to Pytagsup format try [online converter](https://javatagsconverter.fly.dev).

## Usage

Import module `pytagsup.html` in your class.

```python
from pytagsup.html import *

class Layout:  
  #...

```
### Attributes:

You have different ways to use attributes.

#### Declarative

Using Python#Dictionary definition, i.e. `{'name': "value"}` in `attr` method. 

```python
attr({'class': "navbar", 'style': "border: 0;"})
```

#### Dynamic

An attribute can be built fluently with `add` method, using key-value or `Attribute` overload

```python
(
  attr()
  .add({'class': "fa fa-up", 'xxx': "show"})
  .add({'style': "border: 0;"})
)
(	
  attr()
    .add(attr({'class': "navbar"}))
    .add(attr({'style': "border: 0;"}))
)
```

`add` method appends values if already defined for an attribute

```python
attr({'class': "navbar"})
  .add({'class': "fa fa-up"})
  .add({'style': "border: 0;"})
```

renders

```html
 class='navbar fa fa-up' style='border: 0;'
```

An attribute can be modified with remove method, using key-value, Attribute overload or key

```python
attr({'class': ".some fa fa-up", 'xxx': "fa fa-up"})
  .remove({'class': "fa-up"})
  .remove({'xxx': "fa"})
  .remove({'xxx': "fa-up"})
```

renders

```html
class='.some fa' xxx=''
```

```python
attr({'class': ".some fa fa-up", 'xxx': "fa fa-up"}).remove('class')
```

renders

```html
xxx='fa fa-up'
```

see [unit tests](https://github.com/manlioGit/pytagsup/tree/master/tests) for other examples

### Layouts:

An example of page layout:

```python
from pytagsup.html import *

class Layout:

  def __init__(self, title, body):
    self._title = title
    self._body = body
  
  def render(self):
    return (
      html5(
        head(
          meta(attr({'charset': "utf-8"})),
          meta(attr({'http-equiv': "X-UA-Compatible", 'content': "IE=edge"})),
          meta(attr({'name': "viewport", 'content': "width=device-width, initial-scale=1"})),
          title(text(self._title)),
          link(attr({'rel': "stylesheet", 'href': "/css/bootstrap.min.css"})),
          link(attr({'rel': "stylesheet", 'href': "/css/app.css"}))
        ),
        body(
          self._body,
          script(attr({'src': "/js/jquery.min.js"})),
          script(attr({'src': "/js/bootstrap.min.js"}))
        )
      ).render()
    )
```

An example of table using reduce:

```python
data = [{ 'th1': "value1", 'th2': "value2" }, { 'th1': "value3", 'th2': "value4" }]
header = data[0].keys()

table(attr({'class': "table"}),
  thead(
    reduce(
      lambda tr, h: tr.add(th(text(h))),
      header,
      tr()
    )
  ),
  reduce(
    lambda tbody, record: tbody.add(
      reduce(
        lambda row, x: row.add(td(text(record[x]))),
        header,
        tr()
      )
    ),
    data,
    tbody()
  )
)

```

#### Element

Ruby-Tags defines Text, Void, NonVoid and Group elements (see [W3C Recommendation](https://www.w3.org/TR/html/syntax.html#writing-html-documents-elements)).

Every tag method (e.g. html5, body and so on) is defined as method using a Void or NonVoid element in accordance with [W3C Recommendation](https://www.w3.org/TR/html).

To avoid built-in shadowing `builtins` module must be used, e.g.

```python
import builtins

div(*builtins.map(lambda t: p(text(t)), ['x', 'y', 'z']))
```

To render text use `text` method.

```python
text("aaa")
```

To render list of Elements you can use dummy `group` method or directly unpack argument lists 


```python
...
l = builtins.map(lambda t: li(text(t)), ['a', 'b', 'c'])
ul(
  group(*l)
)

...
ul(
  group(*builtins.map(lambda x: li(text(x)), ['a', 'b', 'c']))
)
...

```

You can also use `add` method to add children/sibling to a NonVoid/Void element respectively, for example:

```python
...
g = group()
for x in ['a', 'b', 'c']:
  g.add(li(text(x)))
...
	
ul = ul()
for x in ['a', 'b', 'c']:
  ul.add(li(text(x)))

```
Or in a builder/fluent syntax way:

```python
(
  ul()
    .add(li(text("item 1")))
    .add(li(text("item 2")))
    .add(li(text("item 3")))	
)  
(
  div(attr({'class': "xxx"}))
    .add(span(text("content")))
    .add(p(text("other content")))
)
```

Elements are equal ignoring attribute order definition, for example:

```python
def test_equality(self):
  div1 = NonVoid("div", Attribute({'a': "b", 'c': "d"}))
  div2 = NonVoid("div", Attribute({'c': "d", 'a': "b"}))

  assert div1 == div2
```

see [unit tests](https://github.com/manlioGit/ruby-tags/tree/master/test/pytagsup) for other examples

## Development

After checking out the repo, run `pytest` to run the tests.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/manlioGit/pytagsup.


## License

The package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
