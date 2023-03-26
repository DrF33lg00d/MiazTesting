import json

import peewee
import requests
from tqdm import tqdm

from src.db import PosCat, Question, Answer, init_tables
from utils.settings import URL, POSITION_FORMAT, logger


def main(poscat_id: int):
    init_tables()
    new_question_count: int = 0

    response: requests.Response = requests.post(URL, {'cat_id': poscat_id})
    logger.debug(f'Reponse result: {response.status_code}')
    if response.status_code != 200:
        logger.warning('Bad response status code, closing...')
        exit()

    raw_text: str = (
        response.text
        .encode('cp1251')
        .decode('utf-8')
        )
    data: dict = json.loads(raw_text)['data']
    description_pos = POSITION_FORMAT.format(
        posid=data['pos']['id'],
        catid=data['cat']['id'],
        pos=data['pos']['title'],
        cat=data['cat']['title'],
    )
    pos_cat: tuple[PosCat, bool] = PosCat.get_or_create(
        id=data['cat']['id'],
        description=description_pos.strip(),
        )
    if pos_cat[1]:
        logger.info(f'Add new PosCat, id={pos_cat[0].id}')
    else:
        logger.debug(f'PosCat already exists, id={pos_cat[0].id}')

    for q in tqdm(data['questions'], desc='Questions'):
        try:
            question: tuple[Question, bool] = Question.get_or_create(
                id=q['id'],
                description=q['description'].strip(),
                poscat=pos_cat[0],
            )
            if not question[1]:
                continue
            question: Question = question[0]
        except peewee.IntegrityError:
            question: Question = Question.get_by_id(q['id'])

        new_question_count += 1
        logger.info(f'Add new question, id={question.id}')

        for ans in q['answers']:
            answer: tuple[Answer, bool] = Answer.get_or_create(
                id=ans['id'],
                description=ans['description'].strip(),
                is_correct=float(ans['fraction'])>0.0,
                question=question,
            )
            if answer[1]:
                logger.info(f'Add new answer, id={answer[0].id}')
    if new_question_count:
        logger.info(f'{new_question_count} questions were added')
    print('Complete')
