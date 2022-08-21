import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

address_list = []

def getAddress(shop_name, page_number):
    url = f'https://www.meinprospekt.de/filialen/{shop_name}/{page_number}'
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    address_details = soup.find_all('li', {'itemtype' : 'http://schema.org/LocalBusiness'})
    for address in address_details:

        company_name =  address.find('strong', {'itemprop':'name'}).text
        company_address = address.find('span', {'itemprop' :'streetAddress'}).text
        postal_code = address.find('span', {'itemprop' : 'postalCode'}).text
        location = address.find('span', {'itemprop' : 'addressLocality'}).text
        link = 'https://www.meinprospekt.de' + address.find('a', {'class' : 'mp-address'})['href']

        page = requests.get(link, headers = headers)
        soup = BeautifulSoup(page.text, "html.parser")
        contact_data = soup.find('div', {'itemtype' : 'http://schema.org/LocalBusiness'})

        if contact_data.find('span', {'itemprop' :'telephone'}) == None:
            contact = contact_data.find('span', {'itemprop' :'telephone'})
        else:
            contact = contact_data.find('span', {'itemprop': 'telephone'}).text

        addresses = {
            'company_name': company_name,
            'company_address': company_address,
            'postal_code': postal_code,
            'location': location,
            'link': link,
            'contact' : contact,

        }
        address_list.append(addresses)


    return

for x in range(0, 10):
    getAddress('Edeka', x)
    # getAddress('rewe-de', x)
    # getAddress('kaufland', x)
    # getAddress('edekacenter-de', x)
    # getAddress('real-de', x)
    # getAddress('kupsch-de', x)
    # getAddress('nahundgut-de', x)
    # getAddress('edekazurheide-de', x)
    # getAddress('diska-de', x)
    # getAddress('hit-de', x)
    # getAddress('marktkauf', x)

df = pd.DataFrame(address_list)
df.to_csv('Edeka_all.csv', index = False)
#df.to_csv('rewe-de.csv', index=False)
print('Hey, you did a great job ):')












