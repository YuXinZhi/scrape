import lxml.html

broken_html = '<ul class=country><li>Area<li>Population</ul>'
tree = lxml.html.fromstring(broken_html)    #parse the HTML
fixed_html = lxml.html.tostring(tree,pretty_print=True)
print(fixed_html)

