from peewee import (
    Model, PrimaryKeyField, CharField, ForeignKeyField, BooleanField,
    Database,
    )

from utils.settings import db


class DefaultModel(Model):
    class Meta:
        database = db


class PosCat(DefaultModel):
    id = PrimaryKeyField()
    description = CharField()


class Question(DefaultModel):
    id = PrimaryKeyField()
    description = CharField()
    poscat = ForeignKeyField(PosCat, backref='poscat')


class Answer(DefaultModel):
    id = PrimaryKeyField()
    description = CharField()
    is_correct = BooleanField(default=False)
    question = ForeignKeyField(Question, backref='question')


def init_tables(db: Database = db) -> None:
    db.create_tables([PosCat, Question, Answer])  # type: ignore
    return None
