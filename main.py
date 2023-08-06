import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from os import path


url = 'https://mangalib.me/manga-list?types[]=1'
anime = dict()
items = ['Год релиза', 'Автор', 'Художник', 'Возрастной рейтинг', 'Загружено глав']


def get_html(url):
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(url)
        driver.implicitly_wait(3)
        h_prev = 0
        
        while True:
            h = driver.execute_script('return window.innerHeight + window.scrollY;')
            driver.execute_script(f'window.scrollTo(0,{h});')
            driver.implicitly_wait(1)
            if h == h_prev:
                break

            h_prev = h
    except Exception as ex:
        print(ex)
    finally:
        with open('source-page.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

        driver.close()
        driver.quit()

def parser(anime, items):
    if not path.isfile('source-page.html'):
        get_html(url)
    elif path.isfile('source-page.html'):
        with open('source-page.html', encoding='utf-8') as file:
            src = file.read()

        soup1 = BeautifulSoup(src, 'lxml')
        
        def check_items(title, value):
            if second_data.find('div', class_='media-info-list__title').text in items:
                anime[data.div.h5.text][data.div.h3.text].setdefault(title, value)

        for data in soup1.find_all('a', class_='media-card', href=True):
            try:
                if data.get('href'):
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

        with open('word.txt', 'w', encoding='utf-8') as file:
            for _, first_value in anime.items():
                for second_key, second_value in first_value.items():
                    file.writelines(f'{second_key} ---- {second_value}\n')

if __name__ == '__main__':
    parser(anime, items)
