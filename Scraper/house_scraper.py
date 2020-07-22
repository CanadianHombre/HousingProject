import bs4
import requests
import pandas as pd
from collections import OrderedDict
from datetime import datetime

link = 'https://www.viewknoxvillerealestate.com/search/quick?city=Knoxville%2CTN&daysonsite=3&maxprice=520000&minbeds=1&minprice=40000&page=1&perpage=100&soldproperty=0&sortby=latest&type=quick'
source = requests.get(link).text
soup = bs4.BeautifulSoup(source, 'lxml')

Price = []
for house in soup.find_all('div',class_="card--list-header"):
  houses = house.text
  Price.append(houses)
  
zip_code = [] 
Address = []
for house in soup.find_all('p',class_="full-address"):
  houses = house.text.rsplit(' ',1)
  Address.append(houses[0])
  zip_code.append(houses[1])

Beds = []
Baths = []
Area = []
for house in soup.find_all('div',class_="card--list-stats"):
  houses = house.text.strip()
  info = houses.split('\n')
  Beds.append(info[0].split('B')[0])
  Baths.append(info[1].split('B')[0])
  Area.append(info[2])

df = pd.DataFrame(OrderedDict({'Price':Price, 'Area': Area}))
raw_price = df['Price'].replace({'\$': '', ',': '', 'n/a':'1'}, regex=True)
raw_area =  df['Area'].replace({',':'','SqFt': '','n/a':'1'}, regex=True)
raw_price = [int(i) for i in raw_price]
raw_area = [int(i) for i in raw_area]
Value = [x/y for x, y in zip(raw_price, raw_area)] #Price per square foot
Value = [ '%1.f' % elem for elem in Value ] # rounds numbers to one decimal place
df = pd.DataFrame(OrderedDict({'Zip Code' : zip_code,'Home Address': Address,'Price':raw_price, 'Beds': Beds,
                               'Baths':Baths, 'Area':raw_area , 'Price/sqft': Value }))
df['Price/sqft'] = df['Price/sqft'].astype('int')

# Adds the current Date and Time Column for Tracking purposes
current_date = datetime.date(datetime.now())
df['Name'] = current_date
df.to_csv('HousingData.csv',index = False)