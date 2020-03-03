import peewee
from peewee import *

mysql_db = MySQLDatabase('news', user='root', password='25012000',
                         host='localhost', port=3306)


class MySQLModel(peewee.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db


class eduNew(MySQLModel):
    url = CharField(primary_key=True)
    news_title = CharField()
    news_content = TextField()

    class Meta:
        db_table = 'edunew'


def make_connect():
    mysql_db.connect(reuse_if_open=True)


def createEduNewTab():
    eduNew.create_table()


def insertMultiRecords(datas):
    # Can change the limit based on the max buffer size
    with mysql_db.atomic():
        eduNew.insert_many(datas, fields = [eduNew.url, eduNew.news_title, eduNew.news_content]).execute()


def closeDB():
    if mysql_db.close():
        print("Closed connection with DB")
