import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


# получаем исходный код страницы
def get_sourse_html(url):
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

            # скролим страницу
            else:
                actions = ActionChains(driver)
                actions.click(find_more_element).perform()
                time.sleep(5)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


def main():
    get_sourse_html(
        url='https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10')


if __name__ == '__main__':
    main()
