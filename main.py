import json
import random
import re
import fake_useragent
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import unquote

ua = fake_useragent.UserAgent()
headers = {
    'User-Agent': ua.random
}


def get_sourse_html(url):
    """
    Функция получает исходный код страницы
    :param url: str
    :return:
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()

    try:
        # передаем драйверу url
        driver.get(url=url)
        # ставим паузу, чтобы страница успела прогрузиться
        time.sleep(5)

        while True:
            # находим div в котором расположена кнопка "Показать еще"
            find_more_element = driver.find_element(by=By.CLASS_NAME, value='catalog-button-showMore')
            # проверяем есть ли на странице элемент с классом "hasmore-text"
            if driver.find_elements(by=By.CLASS_NAME, value='hasmore-text'):
                # сохраняем страницу и завершаем работу функции
                with open('source-page.html', 'w', encoding='utf-8') as file:
                    file.write(driver.page_source)

                break

            # скроллим страницу
            else:
                actions = ActionChains(driver)
                actions.click(find_more_element).perform()
                time.sleep(5)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path):
    """
    Функция получает ссылки со всех карточек и сохраняет в файл
    :param file_path: str
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        src = file.read()

    # получаем все карточки со страницы
    soup = BeautifulSoup(src, 'lxml')
    items_div = soup.find_all('div', class_='minicard-item__info')

    urls = []

    # получаем ссылки
    for item in items_div:
        item_url = item.find('h2', class_='minicard-item__title').find('a').get('href')
        urls.append(item_url)

    # записываем  полученные url в файл
    with open('item_urls.txt', 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(f'{url}\n')

    return print('[INFO] urls collected successfully')


def get_data(file_path):
    """
    Функция получает данные с каждой ссылки из item_urls.txt и сохраняет полученные данные в json
    :param file_path: str
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    urls_count = len(urls_list)
    count = 1
    # переходим по каждой ссылке из списка
    for url in urls_list:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        # получаем название мед.учереждения
        try:
            item_name = soup.find('span', {'itemprop': 'name'}).text.strip()
        except Exception as _ex:
            item_name = None

        item_phones_list = []
        # получаем номера телефонов
        try:
            item_phones = soup.find('div', class_='service-phones-list').find_all('a', class_='js-phone-number')

            for phone in item_phones:
                item_phone = phone.get('href').split(':')[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as _ex:
            item_phones_list = None

        # получаем адрес
        try:
            item_address = soup.find('address', class_='iblock').text.strip()
        except Exception as _ex:
            item_address = None

        # получаем ссылку на сайт учереждения
        try:
            item_site = soup.find(text=re.compile('Сайт|Официальный сайт')).find_next().text.strip()
        except Exception as _ex:
            item_site = None

        social_networks_list = []
        # получаем ссылки на соцсети
        try:
            item_social_networks = soup.find(text=re.compile('Страница в соцсетях')).find_next().find_all("a")
            for sn in item_social_networks:
                sn_url = sn.get('href')
                sn_url = unquote(sn_url.split('?to=')[1].split('&')[0])
                social_networks_list.append(sn_url)
        except Exception as _ex:
            social_networks_list = None

        result_list.append(
            {
                'item_name': item_name,
                'item_url': url,
                'item_phones_list': item_phones_list,
                'item_address': item_address,
                'item_site': item_site,
                'social_networks_list': social_networks_list
            }
        )

        time.sleep(random.randrange(2, 5))

        if count % 10 == 0:
            time.sleep(random.randrange(5, 9))

        print(f'[+] Processed: {count}/{urls_count}')

        count += 1

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    return '[INFO] Data collected successfully!'


def main():
    get_sourse_html(
        url='https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10')
    get_items_urls(file_path='source-page.html')
    get_data(file_path='item_urls.txt')


if __name__ == '__main__':
    main()
