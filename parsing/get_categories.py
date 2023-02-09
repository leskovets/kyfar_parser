from database.db_hendler import add_category, check_category
import requests
from bs4 import BeautifulSoup


def parsing_categories() -> None:
    url_template = 'https://www.kufar.by/l'
    r = requests.get(url_template)
    soup = BeautifulSoup(r.text, "html.parser")
    categories = soup.find_all("a", class_='styles_element__CgYpE')
    for category in categories[2:]:
        if not check_category(category.text):
            add_category(name=category.text, url='https://www.kufar.by' + category.get('href'))
        parsing_subcategories(name=category.text, url='https://www.kufar.by' + category.get('href'))


def parsing_subcategories(name: str, url: str) -> None:
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "html.parser")
    categories = soup.find_all("div", class_='styles_wrapper__GXcQ2')
    if len(categories) > 1:
        categories = categories[1].find_all("a", class_='styles_link__wrapper__S6cxw')
        for category in categories:
            if not check_category(category.text):
                add_category(name=category.text, url='https://www.kufar.by' + category.get('href'), father_name=name)
            parsing_sub_sub_categories(name=category.text, url='https://www.kufar.by' + category.get('href'))


def parsing_sub_sub_categories(name: str, url: str) -> None:
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "html.parser")
    categories = soup.find_all("div", class_='styles_wrapper__GXcQ2')
    if len(categories) > 2:
        categories = categories[2].find_all("a", class_='styles_link__wrapper__S6cxw')
        for category in categories:
            if not check_category(category):
                add_category(name=category.text, url='https://www.kufar.by' + category.get('href'), father_name=name)



