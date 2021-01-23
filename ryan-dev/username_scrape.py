from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

def scrape_for_user(url):
    """This function checks and accepts a Yahoo finance URL and outputs the Total ESG Risk Score as an int """

    #GET page and convert content to bs4 soup
    session = HTMLSession()
    page = session.get(url)
    page.html.render()
    soup = page.html.find('@').text
    #soup = BeautifulSoup(page.content, 'html.parser')

    # #Find class containing ESG risk score from 0-100, cast to string
    # total_ESG = str(soup.findAll('div', {"class": "Fz(36px) Fw(600) D(ib) Mend(5px)"}))
    #
    # #Extract ESG score using regex, with error handling
    # if total_ESG != '[]':
    #     total_ESG = int(re.search('data-reactid="20">(.+?)</div>', total_ESG).group(1))
    # else:
    #     total_ESG = None

    return soup

#Testing
print(scrape_for_user("https://twitter.com/WhiteHouse?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"))