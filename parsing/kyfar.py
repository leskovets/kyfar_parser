import requests
import re
from bs4 import BeautifulSoup


def get_advertisements(text: str, price_range: str) -> list:

    text = text.split(",")
    price = price_range.split(",")

    url_templates = []
    for el in text:
        url_templates.append("https://www.kufar.by/l?cnd=1&prc=r%3A{}00%2C{}00&query={}&sort=lst.d".format(
            price[0],
            price[1],
            "+".join(el.split())))

    advertisements_list = []
    for url_template in url_templates:
        r = requests.get(url_template)
        soup = BeautifulSoup(r.text, "html.parser")
        advertisements = soup.find_all("a", class_='styles_wrapper__IMYdY')

        for advertisement in advertisements:
            id_advertisement = re.search(r"[0-9]{7,10}", advertisement.get('href')).group()
            continue_branch = False
            for el in advertisements_list:
                if el['id'] == id_advertisement:
                    continue_branch = True
                    break
            if continue_branch:
                continue
            price = advertisement.find('p', class_='styles_price__tiO8k').text
            if price == "Договорная" or price == "Бесплатно":
                price = 0
            else:
                price = re.search(r"[0-9]{1,3} р|[0-9]{1,3} [0-9]{3} р|[0-9]{1,3} [0-9]{3} [0-9]{3} р", price).group()
                price = ''.join(price[:-2].split())

            advertisements_list.append({
                'linc': advertisement.get('href'),
                'title': advertisement.find('h3', class_='styles_title__XS_QS').text,
                'price': int(price),
                'id': id_advertisement
            })

    return sorted(advertisements_list, key=lambda el: el['price'])
