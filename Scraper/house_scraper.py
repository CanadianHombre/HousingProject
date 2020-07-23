import datetime as dt
import urllib.parse as urlparse

import bs4
import pandas as pd
import requests


def parse_nums(text, cast_to=int):
    try:
        return cast_to(''.join(n for n in text if n.isdigit()))
    except ValueError:
        return None


def main_scraper(query):
    url = 'https://www.viewknoxvillerealestate.com/search/quick'
    r = requests.get(url, params=query)
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    all_homes = []
    for card in soup('div', 'card--list'):
        beds, baths, sqft = (parse_nums(li.text) for li in card('li'))
        home = {
            'address'   : card.find('p', 'full-address').text,
            'zip_code'  : card.find('p', 'full-address').text.split(' ')[-1],
            'price'     : parse_nums(card.find('div', 'card--list-header').text),
            'price_sqft': None,
            'sqft'      : sqft,
            'beds'      : beds,
            'baths'     : baths,
            'url'       : urlparse.urljoin(url, card.a['href']),
        }
        if home['price'] and home['sqft']:
            home['price_sqft'] = home['price'] // home['sqft']

        all_homes.append(home)

    return all_homes


def main():
    query = {
        'city'        : 'Knoxville,TN',
        'daysonsite'  : 2,
        'maxprice'    : 520000,
        'minbeds'     : 1,
        'minprice'    : 40000,
        'page'        : 1,
        'perpage'     : 10000,
        'soldproperty': 0,
        'sortby'      : 'latest',
        'type'        : 'quick',
    }
    data = []
    data.extend(main_scraper(query))
    df = pd.DataFrame(data)
    df['date_scraped'] = dt.date.today()
    df.to_csv('HousingData.csv', index=False)


if __name__ == '__main__':
    main()