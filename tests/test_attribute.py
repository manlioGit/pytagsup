from test_helper import *
from pytagsup.attribute import Attribute
from pytagsup.html import attr

class TestAttribute:
  
  def test_render(self):
    assert_render(" id='123' class='fa fa-up'", Attribute({'id': "123", 'class': "fa fa-up"}))
    assert_render(" id='123' class='fa fa-up'", attr({'id': 123, 'class': "fa fa-up"}))
    
  def test_render_normalize_spaces(self):
    assert_render(" id='123' class='fa fa-up'", attr({'id': "  123 ", 'class': " fa      fa-up "}))

  def test_dont_render_null_or_empty_keys(self):
    a = attr({
      'id': 123,
      "xx": None,
      'class': "fa fa-up",
      None: "xx",
      'x': "",
      " ": "xx"
    })
    
    assert_render(" id='123' class='fa fa-up' x=''", a)

  def test_add_attribute_using_dict(self):
    a = (
      attr({'class': "some", 'xxx':"fa fa-up"})
        .add({'class': "fa fa-up", 'xxx': "show"})
        .add({'class': "fa", 'xxx': "show"})
        .add(None)
        .add({'xxx': "hide"})
        .add({'xxx': None})
        .add({None: None})
        .add({'yyy': "show-some"})
    )
    
    assert_render(" class='some fa fa-up' xxx='fa fa-up show hide' yyy='show-some'", a)
  
  def test_add_attribute_using_attribute(self):
    a = (
      attr({'class': "some", 'xxx':"fa fa-up"})
        .add(attr({'class': "fa fa-up"}))
        .add(attr(None))
        .add(attr({'xxx': "hide"}))
        .add(attr({'xxx': "show", 'yyy': "show-some"}))
    )

    assert_render(" class='some fa fa-up' xxx='fa fa-up hide show' yyy='show-some'", a)

  def test_remove_attribute_using_dict(self):
    a = (
      attr({'class': ".some fa fa-up", 'xxx': "fa fa-up"})
        .remove({'class': "fa-up"})
        .remove(None)
        .remove({'class': "notExistent"})
        .remove({'xxx': "fa"})
        .remove({'xxx': None})
        .remove({None: None})
        .remove({'xxx': "fa-up"})
        .remove({'xxx': "fa-up"})
        .remove({'notExistentKey': "show-some"})
    )

    assert_render(" class='.some fa' xxx=''", a)
    assert_render(" class='.some'", attr({'class': ".some fa fa-up"}).remove({'class':"fa fa-up"}))
    assert_render(" class='.some fa fa-up'", attr({'class': ".some fa fa-up"}).remove({None: None}))

  def test_remove_using_attribute(self):
    a = (
      attr({'class': ".some fa fa-up", 'xxx': "fa fa-up"})
        .remove(attr({'class': "fa-up"}))
        .remove(attr({'class': "notExistent"}))
        .remove(attr({'xxx': "fa"}))
        .remove(attr(None))
        .remove(attr({'xxx': "fa-up"}))
        .remove(attr({'xxx': "fa-up"}))
        .remove(attr({'notExistentKey': "show-some"}))
    )
    assert_render(" class='.some fa' xxx=''", a)
  
  def test_complete_removal(self):
    a = (
      attr({'class': ".some fa fa-up", 'xxx': "fa fa-up"})
        .remove('class')
        .remove('xxx')
    )

    assert_render("", a)

  def test_equality(self):
    a = attr({'class': ".some fa fa-up", 'xxx': "fa fa-up"})
    b = attr({'xxx': "fa fa-up", 'class': ".some fa fa-up"})
    c = ( 
      attr().add({'xxx': "fa"}).add({'xxx': "fa-up"}).add({'class': "fa"})
            .add({'class': ".some"}).add({'class': "fa-up"})
    )

    assert a == b
    assert b == c
    assert a == c
    assert a != b.add({'x': 12})

  def test_sanitize(self):
    assert_render(" value='1&#x27;000'", attr({'value': "1'000"}))
  
  def test_empty_attribute(self):
    assert_render("", attr())