from test_helper import *
from pytagsup.tags import Group, Void

class TestGroup:

  def test_equality(self):
    g1 = Group(Void("br"))
    g2 = Group(Void("br"))

    assert g1 == g2

  def test_add(self):
    g = (
      Group(Void("br"))
        .add(Void("div"))
        .add(Void("span"))
    )

    assert_render("<br/><div/><span/>", g)