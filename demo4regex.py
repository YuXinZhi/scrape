import re
import demo3downloadwebpage
from bs4 import BeautifulSoup
url = "http://example.webscraping.com/places/default/view/United-Kingdom-239"
html = demo3downloadwebpage.download(url)
result = re.findall('<td class="w2p_fw">(.*?)</td>',html)[1]
print(result)



