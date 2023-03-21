import sqlite3

from peewee import (
    Model, PrimaryKeyField, CharField, ForeignKeyField, BooleanField,
    Database,
    )

from settings import db, db_settings


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


init_tables()


class DB:
    def __init__(self):
        self.con = sqlite3.connect(db_settings.get('name', 'sample.db'))

    def close(self):
        self.con.close()
        del self

    def add_question(self, id_title: int, id_global_que: int, description: str) -> bool:
        result = True
        cursor = self.con.cursor()
        query = '''INSERT INTO question (id_title, id_global_que, description)
                    VALUES ('{0}','{1}','{2}')'''
        try:
            cursor.execute(query.format(id_title, id_global_que, description))
            self.con.commit()
        except sqlite3.Error as error:
            print(error)
            result = False
        finally:
            cursor.close()
        return result

    def add_answer(self, id_global_ans: int, id_question: int, description: str, is_correct: bool) -> bool:
        result = True
        cursor = self.con.cursor()
        query = '''INSERT INTO answer (id_q, id_global_ans, description, is_correct)
                    VALUES ('{0}','{1}','{2}', '{3}')'''
        try:
            cursor.execute(query.format(id_question, id_global_ans, description, is_correct))
            self.con.commit()
        except sqlite3.Error as error:
            print(error)
            result = False
        finally:
            cursor.close()
        return result

    def get_question_id(self, id_global_que: int) -> int or None:
        result = None
        cursor = self.con.cursor()
        query = '''SELECT id FROM question WHERE id_global_que={}'''
        try:
            cursor.execute(query.format(id_global_que))
            result = cursor.fetchone()[0]
        except (sqlite3.Error, IndexError, TypeError) as error:
            pass
        finally:
            cursor.close()
        return result

    def get_answer_id(self, id_global_ans: int) -> int or None:
        result = None
        cursor = self.con.cursor()
        query = '''SELECT id FROM answer WHERE id_global_ans={}'''
        try:
            cursor.execute(query.format(id_global_ans))
            result = cursor.fetchone()[0]
        except (sqlite3.Error, IndexError, TypeError) as error:
            pass
        finally:
            cursor.close()
        return result

    def get_all_questions(self) -> dict:
        result = None
        cursor = self.con.cursor()
        query = '''SELECT id, description FROM question'''
        try:
            cursor.execute(query)
            result = [{'id': item[0],
                       'description': item[1]} for item in cursor.fetchall()]
        except (sqlite3.Error, IndexError, TypeError) as error:
            pass
        finally:
            cursor.close()
        return result

    def get_all_answers(self, id_question: int) -> list:
        result = None
        cursor = self.con.cursor()
        query = '''SELECT id, description, is_correct FROM answer WHERE id_q={}'''
        try:
            cursor.execute(query.format(id_question))
            result = [
                {
                    'id': item[0],
                    'description': item[1],
                    'is_correct': 'true' in item[2].lower()
                }
                for item in cursor.fetchall()]
        except (sqlite3.Error, IndexError, TypeError) as error:
            pass
        finally:
            cursor.close()
        return result


db = DB()
