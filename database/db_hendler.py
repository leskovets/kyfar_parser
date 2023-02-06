from .models import User, Advertisement, Search_request


def add_user(chat_id: int, status: str) -> None:
    User(chat_id=chat_id, status=status).save()


def get_user(chat_id: int) -> list:
    return [x for x in User.select().where(User.chat_id == chat_id)]


def add_advertisement(chat_id: int, advertisement_id: int,
                      search: Search_request, text: str, price: int) -> None:
    Advertisement(chat_id=chat_id,
                  advertisement_id=advertisement_id,
                  search=search,
                  text=text,
                  price=price).save()


def get_advertisement(chat_id: int) -> list:
    return [x for x in Advertisement.select().where(Advertisement.chat_id == chat_id)]


def check_advertisement(chat_id: int, advertisement_id: int) -> list:
    return [x for x in Advertisement.select().where(
        Advertisement.chat_id == chat_id and Advertisement.advertisement_id == advertisement_id)]


def add_search_request(chat_id: int, text: str, price_range: str) -> None:
    Search_request(chat_id=chat_id, text=text, price_range=price_range).save()


def get_search_request() -> list:
    return [x for x in Search_request.select()]


def delete_search_request(id_req: int) -> None:
    req = Search_request.get(Search_request.id == id_req)
    req.delete_instance()


def get_search_user_request(chat_id: int) -> list:
    return [x for x in Search_request.select().where(Search_request.chat_id == chat_id)]
