from .models import User, Advertisement, Search_request, Category


def add_user(chat_id: int, status: str) -> None:
    User(chat_id=chat_id, status=status).save()


def get_user(chat_id: int) -> list:
    return [x for x in User.select().where(User.chat_id == chat_id)]


def add_advertisement(chat_id: int, advertisement_id: int,
                      search: Search_request, title: str, price: int) -> None:
    Advertisement(chat_id=chat_id,
                  advertisement_id=advertisement_id,
                  search=search,
                  title=title,
                  price=price).save()


def get_advertisement(chat_id: int) -> list:
    return [x for x in Advertisement.select().where(Advertisement.chat_id == chat_id)]


def check_advertisement(chat_id: int, advertisement_id: int) -> list:
    return [x for x in Advertisement.select().where(
        Advertisement.chat_id == chat_id and Advertisement.advertisement_id == advertisement_id)]


def add_search_request(chat_id: int, title: str, search_text: str, price_min: str, price_max) -> None:
    Search_request(chat_id=chat_id, title=title, search_text=search_text,
                   price_min=price_min, price_max=price_max).save()


def update_search_request(chat_id: int, title: str, command: str, new_value: str) -> None:
    search = get_search_request_user_title(chat_id=chat_id, title=title)
    if command == 'title':
        search.title = new_value
    if command == 'text':
        search.search_text = new_value
    if command == 'min':
        search.price_min = new_value
    if command == 'max':
        search.price_max = new_value
    search.save()


def get_search_request() -> list:
    return [x for x in Search_request.select()]


def delete_search_request(title: str) -> None:
    req = Search_request.get(Search_request.title == title)
    req.delete_instance()


def get_search_request_user(chat_id: int) -> list:
    return [x for x in Search_request.select().where(Search_request.chat_id == chat_id)]


def get_search_request_user_title(chat_id: int, title: str) -> Search_request:
    return Search_request.get(Search_request.chat_id == chat_id, Search_request.title == title)


def check_search_request_user_title(chat_id: int, title: str) -> bool:
    if len(Search_request.select().where(Search_request.chat_id == chat_id, Search_request.title == title)):
        return True
    return False


def get_search_text_request(text: str) -> Search_request:
    return Search_request.get(Search_request.search_text == text)


def add_category(name: str, url: str, father_name: str = None) -> None:
    Category(name=name, url=url, father_name=father_name).save()


def check_category(name: str) -> bool:
    if len(Category.select().where(Category.name == name)):
        return True
    return False


def get_categories(name: str = None) -> list:
    return Category.select().where(Category.name == name)
