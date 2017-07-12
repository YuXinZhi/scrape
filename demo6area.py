from bs4 import BeautifulSoup
import demo3downloadwebpage

url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = demo3downloadwebpage.download(url)
soup = BeautifulSoup(html,'html.parser')
#print(soup.prettify())

#locate the area row
tr = soup.find(attrs={'id':'places_area__row'})
td = tr.find(attrs={'class':'w2p_fw'}) #locate the area tag
area = td.text #extract the text from this tag
print(area)
