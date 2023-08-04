import requests
from bs4 import BeautifulSoup
import json

url = 'https://mangalib.me/manga-list?types[]=1'
page = requests.get(url)
soup1 = BeautifulSoup(page.text, "lxml")
anime = dict()
items = ['Год релиза', 'Автор', 'Художник', 'Возрастной рейтинг', 'Загружено глав']

def check_items(title, value):
    if second_data.find('div', class_='media-info-list__title').text in items:
        anime[data.div.h5.text][data.div.h3.text].setdefault(title, value)

for data in soup1.find_all('a', class_='media-card', href=True):
    try:
        anime.setdefault(data.div.h5.text, {}).setdefault(data.div.h3.text, {}).setdefault('href', data.get('href'))
        redirect = requests.get(data.get('href'))
        soup2 = BeautifulSoup(redirect.text, 'lxml')
        for second_data in soup2.find_all('a', class_='media-info-list__item'):            
            check_items(second_data.find('div', class_='media-info-list__title').text, second_data.find('div', class_='media-info-list__value').text)
        
        for second_data in soup2.find_all('div', class_='media-info-list__item'):
            check_items(second_data.find('div', class_='media-info-list__title').text, second_data.find('div', class_='media-info-list__value').text.strip('\n'))

    except Exception as ex:
        print(f'{ex} ------> Maybe the data field is empty')
        continue

print(anime.json())

# with open('word.txt', 'w') as file:
#     for first_key, first_value in anime.items():
#         for second_key, second_value in first_value.items():
#             file.writelines(f'{second_key} ---- {second_value}\n')
