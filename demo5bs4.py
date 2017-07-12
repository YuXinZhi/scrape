from bs4 import BeautifulSoup
broken_html = '<ul class=country><li>Area<li>Population</ul>'
#parse the html
soup = BeautifulSoup(broken_html,'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

