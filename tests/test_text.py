from test_helper import *
from pytagsup.tags import Text

class TestText:

  def test_equality(self):
    assert Text("aaa") == Text("aaa")
    assert Text("aaa") != Text("bbb")
    assert Text("aaa") != None
   
  def test_render(self):
   assert_render("aaa", Text("aaa"))
  