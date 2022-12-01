import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://en.wikipedia.org/wiki/IPhone'
text = requests.get(url).text.encode('utf-8')

soup = BeautifulSoup(text, 'lxml')
table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')[1:]

iphone_price = {}

for row in rows:
    data = row.find_all(['th','td'])
    try:
        version_txt = data[0].a.text.split(' ')[1]
        version = re.sub(r"\D", "", version_txt)
        # print(version)
        price_txt = data[-1].text.split('/')[-1]
        price = re.sub(r"\D", "", price_txt)
        price = int(price)
        if version and price > 100:
            iphone_price[version] = price
    except:
        pass


print(iphone_price)
csv_fields = ['version', 'price']

with open('iphone_price.csv', 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(csv_fields)
    for key,value in iphone_price.items():
        csvwriter.writerow([key,value])