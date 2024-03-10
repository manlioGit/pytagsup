from test_helper import *
from pytagsup.tags import Group, NonVoid, Text
from pytagsup.attribute import Attribute

class TestNonVoid:

  def test_simple_tag(self):
    assert_render("<html></html>", NonVoid("html"))
  
  def test_simple_tag_with_attribute(self):
    assert_render("<div id='123' class='x'></div>", NonVoid("div", Attribute({'id': 123, 'class': "x"})))
    assert_render("<div id='123'></div>", NonVoid("div", Attribute({'id': "123"})))
  
  def test_simple_tag_with_text(self):
    assert_render("<div>text</div>", NonVoid("div", Text("text")))
    assert_render("<div id='123' class='x'>text</div>", NonVoid("div", Attribute({'id': 123, 'class': "x"}), Text("text")))
  
  def test_nested_tag(self):
    assert_render("<div><span></span></div>", NonVoid("div", NonVoid("span")))
    assert_render("<div id='123'><span></span></div>", NonVoid("div", Attribute({'id': "123"}), NonVoid("span")))
    assert_render("<div><span id='123'></span></div>", NonVoid("div", NonVoid("span", Attribute({'id': "123"}))))
  
  def test_nested_tag_with_text(self):
    assert_render("<div><span>text</span></div>", NonVoid("div", NonVoid("span", Text("text"))))
  
  def test_text_and_nested_tag(self):
    assert_render("<div>text<span></span></div>", NonVoid("div", Text("text"), NonVoid("span")))
  
  def test_nested_tag_and_text(self):
    tag = NonVoid("div", NonVoid("span"), Text("text"))

    assert_render("<div><span></span>text</div>", tag)
  
  def test_sibling_tags(self):
    tag = Group(Text("<!DOCTYPE html>"), NonVoid("html"))

    assert_render("<!DOCTYPE html><html></html>", tag)
  
  def test_equality(self):
    div1 = NonVoid("div", Attribute({'a': "b", 'c': "d"}))
    div2 = NonVoid("div", Attribute({'c': "d", 'a': "b"}))

    assert div1 == div2
  
  def test_add(self):
    nonVoid = (
      NonVoid("div")
        .add(NonVoid("span"))
        .add(NonVoid("span"))
        .add(NonVoid("span"))
        .add(NonVoid("div"))
    )

    assert_render("<div><span></span><span></span><span></span><div></div></div>", nonVoid)
