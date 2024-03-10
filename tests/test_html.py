from functools import reduce
from test_helper import *
from pytagsup.html import *

class TestHtml:

  def test_html5_with_doc_type(self):
    assert_render("<!DOCTYPE html><html></html>", html5())
    assert_render("<!DOCTYPE html><html class='xxx'></html>", html5(attr({'class': "xxx"})))

  def test_void_elements(self):
    assert_render("<area/>", area())
    assert_render("<area class='xxx'/>", area(attr({'class': "xxx"})))

  def test_non_void_elements(self):
    assert_render("<body></body>", body())
    assert_render("<body class='xxx'></body>", body(attr({'class': "xxx"})))
    
  def test_div_with_attribute_and_text(self):
    assert_render("<div id='123'>some text</div>", div(attr({'id': "123"}), text("some text")))

  def test_text_last_sibling(self):
    div1 = div(div(),text("text"))
    div2 = div(div(),div(),text("text"))

    assert_render("<div><div></div>text</div>", div1)
    assert_render("<div><div></div><div></div>text</div>", div2)

  def test_nested(self):
    frag = html5(
             div(attr({'class': "fa fa-up"}),
               div(attr({'id': "123"}), text("some text"))
             ),
             div(
               br(),
               text("otherText")
             )
           )

    exp = (
      "<!DOCTYPE html>"
      "<html>"
        "<div class='fa fa-up'>"
          "<div id='123'>some text</div>"
        "</div>"
        "<div>"
          "<br/>otherText"
        "</div>"
      "</html>"
    )
    assert_render(exp, frag)

  def test_head_block(self):
    frag = html5(attr({'lang': "en"}),
             head(
               meta(attr({'http-equiv': "Content-Type", 'content': "text/html; charset=UTF-8"})),
               title(text("title")),
               link(attr({'href': "xxx.css", 'rel': "stylesheet"}))
             )
           )

    exp = (
      "<!DOCTYPE html>"
      "<html lang='en'>"
        "<head>"
          "<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>"
          "<title>title</title>"
          "<link href='xxx.css' rel='stylesheet'/>"
        "</head>"
      "</html>"
    )

    assert_render(exp, frag)

  def test_js_on_attribute(self):
    frag = div(
      a(attr({'href': "xxx", 'onclick': 'alert("yay!")'}), text("xxx"))
    )
    assert_render("""<div><a href='xxx' onclick='alert("yay!")'>xxx</a></div>""", frag)

  def test_js_within_script(self):
    s = script(attr({'type': "text/javascript"}), text(
            "function xxx(){"
              "alert('yay!');"
            "}"
          )
        )

    assert_render("<script type='text/javascript'>function xxx(){alert('yay!');}</script>", s)

  def test_table_component(self):
    data = [{ 'th1': "value1", 'th2': "value2" }, { 'th1': "value3", 'th2': "value4" }]
    header = data[0].keys()

    t = table(attr({'class': "table"}),
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

    assert_render(
      "<table class='table'>"
        "<thead>"
          "<tr><th>th1</th><th>th2</th></tr>"
        "</thead>"
        "<tbody>"
          "<tr><td>value1</td><td>value2</td></tr>"
          "<tr><td>value3</td><td>value4</td></tr>"
        "</tbody>"
      "</table>",
      t
    )

  def test_avoid_builtin_shadowing(self):
    import builtins

    assert_render(
      "<ul>"
        "<li>a</li>"
        "<li>b</li>"
        "<li>c</li>"
      "</ul>",
      ul(*builtins.map(lambda t: li(text(t)), ['a', 'b', 'c']))  
    )
