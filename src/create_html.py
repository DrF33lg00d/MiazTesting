import click
from tqdm import tqdm

from src.db import PosCat, Question, Answer, init_tables
from utils.settings import logger, POSCAT_ID


def main(poscat_id: int, filename: click.File):
    init_tables()
    print('Create file')

    logger.info(f'Start creating file with {filename}')
    poscat: PosCat = PosCat.get(id=poscat_id)
    if not poscat:
        logger.critical(f'Cat_id {poscat_id} not found!')
        exit()

    questions: list[Question] = [que for que in (Question
         .select(Question, PosCat)
         .join(PosCat)
         .where(Question.poscat == poscat)
         .order_by(Question.description.asc())
         )]
    logger.debug(f'Count of questions in db: {len(questions)}')
    filename.write('<html><head><title>Answers</title></head>')
    filename.write('<body>')
    for question in tqdm(questions, desc='Questions'):
        answers: list[Answer] = [answer for answer in (Answer
            .select(Answer, Question)
            .join(Question)
            .where(Answer.question == question)
            .order_by(Answer.id.asc())
            )]
        for question in questions:
            filename.write(f'<em>{question.description}</em><br>')
            filename.write('<ul>')
            for answer in answers:
                if answer.is_correct:
                    filename.write(f'<li><b>{answer.description}</b></li>')
                else:
                    filename.write(f'<li>{answer.description}</li>')
            filename.write('</ul>')
            filename.write('<br>')
    filename.write('</body>')
    filename.write('</html>')
    logger.info(f'File {filename} created')
