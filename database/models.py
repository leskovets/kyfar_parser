from peewee import *

db = SqliteDatabase('history.db',  pragmas={'foreign_keys': 1})


def db_init() -> None:
    with db:
        tables = [User, Advertisement, Search_request, Category]
        if not all(table.table_exists() for table in tables):
            db.create_tables(tables)  # создаем таблицы


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Search_request(BaseModel):
    id = IntegerField(primary_key=True)
    chat_id = IntegerField()
    title = CharField(max_length=50)
    search_text = TextField()
    price_min = IntegerField()
    price_max = IntegerField()

    class Meta:
        db_table = "search requests"


class Advertisement(BaseModel):
    id = IntegerField(primary_key=True)
    chat_id = IntegerField()
    advertisement_id = IntegerField()
    search = ForeignKeyField(Search_request, related_name='pets', on_delete='cascade', on_update='cascade')
    title = TextField()
    price = IntegerField()

    class Meta:
        db_table = "advertisements"


class User(BaseModel):
    id = IntegerField(primary_key=True)
    chat_id = IntegerField()
    status = CharField(max_length=50)
    pay = IntegerField()

    class Meta:
        db_table = "users"


class Category(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=50)
    url = CharField(max_length=100)
    father_name = CharField(max_length=50, null=True)

    class Meta:
        db_table = "categories"
