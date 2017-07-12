from bs4 import BeautifulSoup,BeautifulStoneSoup
broken_html = '<ul class=country><li>Area<li>Population</ul>'
#parse the html
soup = BeautifulSoup(broken_html,'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

ul = soup.find('ul',attrs={'class':'country'})
print(ul.find('li'))   #return just the first match
print(ul.find_all('li'))