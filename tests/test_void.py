from test_helper import *
from pytagsup.attribute import Attribute
from pytagsup.tags import Void

class TestVoid:

  def test_has_self_closing_char(self):
    assert_render("<br/>", Void("br"))

  def test_has_self_closing_char_with_attribute(self):
    assert_render("<hr aaa='xxx'/>", Void("hr", Attribute({'aaa': "xxx"})))

  def test_equality(self):
    br1 = Void("br", Attribute({'a': "b", 'c': "d"}))
    br2 = Void("br", Attribute({'c': "d", 'a': "b"}))

    assert br1 == br2
