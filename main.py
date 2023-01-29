import requests
from bs4 import BeautifulSoup
from selenium import webdriver


# получаем исходный код страницы
def get_sourse_html(url):
    driver = webdriver.Chrome(
        executable_path='chromedriver/geckodriver.exe'
    )
    driver.maximize_window()
    try:
        pass
    except Exception as ex:
        print(ex)
    finally:
        driver.close()


def main():
    get_sourse_html()


if __name__ == '__main__':
    main()
