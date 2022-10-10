import requests

from db import db
import settings


count = 0


if '__main__' == __name__:
    data = requests.post(settings.url, {'cat_id': settings.id})
    for que in data.json()['data']['questions']:
        que_db = db.get_question_id(que['id'])
        if que_db:
            count += 1
            continue
        db.add_question(
            que['title'],
            que['id'],
            que['description']
        )
        que_db = db.get_question_id(que['id'])
        for ans in que['answers']:
            ans_id = db.get_answer_id(ans['id'])
            if ans_id:
                continue
            db.add_answer(
                ans['id'],
                que_db,
                ans['description'],
                float(ans['fraction']) > 0.0
            )
    print(f'{count} questions were skipped')
