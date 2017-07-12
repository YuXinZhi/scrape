import lxml.html
import demo3downloadwebpage
'''
CSSx选择器：
    选择所有标签：*
    选择<a>标签：a
    选择所有class="link"的元素：.link
    选择class="link"的<a>标签：a.link
    选择id="home"的<a>标签：a > span
    选择父元素为<a>标签的所有<span>子标签：a > span
    选择<a>标签内部所有<span>子标签：a span
    选择title属性为"Home"的所有<a>标签：a[title=Home]
    
    ***注意：
        lxml在内部实现中，实际上是将CSS选择器转换为等价的XPath选择器
        
'''


url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = demo3downloadwebpage.download(url)
tree = lxml.html.fromstring(html)    #parse the HTML
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
area = td.text_content()
print(area)