import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


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


def main():
    # get_sourse_html(
    #     url='https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10')
    get_items_urls(file_path='source-page.html')

if __name__ == '__main__':
    main()
