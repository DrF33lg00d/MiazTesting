import json

import requests

from db import PosCat, Question, Answer, init_tables
import settings


count: int = 0
POSITION_FORMAT: str = '{posid}-{catid} | {pos} | {cat}'


if '__main__' == __name__:
    raw_response: str = (
        requests.post(settings.url, {'cat_id': settings.id})
        .text
        .encode('cp1251')
        .decode('utf-8')
        )
    data: dict = json.loads(raw_response)['data']
    description_pos = POSITION_FORMAT.format(
        posid=data['pos']['id'],
        catid=data['cat']['id'],
        pos=data['pos']['title'],
        cat=data['cat']['title'],
    )
    pos_cat: tuple[PosCat, bool] = PosCat.get_or_create(
        id=data['cat']['id'],
        description=description_pos,
        )

    for q in data['questions']:
        question: tuple[Question, bool] = Question.get_or_create(
            id=q['id'],
            description=q['description'],
            poscat=pos_cat[0],
        )
        if not question[1]:
            count += 1
            continue

        for ans in q['answers']:
            answer: tuple[Answer, bool] = Answer.get_or_create(
                id=ans['id'],
                description=ans['description'],
                is_correct=float(ans['fraction'])>0.0,
                question=question[0],
            )
    print(f'{count} questions were skipped')
