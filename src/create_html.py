from src.db import PosCat, Question, Answer, init_tables
from utils.settings import logger, POSCAT_ID


def main():
    init_tables()
    print('Create file')

    logger.info('Start creating file with answers.html')
    poscat: PosCat = PosCat.get(id=POSCAT_ID)
    if not poscat:
        logger.critical(f'Cat_id {POSCAT_ID} not found!')
        exit()

    questions: list[Question] = [que for que in (Question
         .select(Question, PosCat)
         .join(PosCat)
         .where(Question.poscat == poscat)
         .order_by(Question.description.asc())
         )]
    logger.debug(f'Count of questions in db: {len(questions)}')
    with open('answers.html', 'w', encoding='utf-8') as f:
        f.write('<html><head><title>Answers</title></head>')

        f.write('<body>')
        for question in questions:
            answers: list[Answer] = [answer for answer in (Answer
                .select(Answer, Question)
                .join(Question)
                .where(Answer.question == question)
                .order_by(Answer.id.asc())
                )]
            for question in questions:
                f.write(f'<em>{question.description}</em><br>')
                f.write('<ul>')
                for answer in answers:
                    if answer.is_correct:
                        f.write(f'<li><b>{answer.description}</b></li>')
                    else:
                        f.write(f'<li>{answer.description}</li>')
                f.write('</ul>')
                f.write('<br>')
        f.write('</body>')
        f.write('</html>')
    logger.info('File answers.html created')


if '__main__' == __name__:
    main()
