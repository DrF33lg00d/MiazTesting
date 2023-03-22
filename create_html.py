from db import PosCat, Question, Answer, init_tables
from utils.settings import logger, POSCAT_ID


if '__main__' == __name__:
    init_tables()
    print('Create file')

    logger.info('Start creating file with answers.html')
    poscat: PosCat = PosCat.get(id=POSCAT_ID)
    if not poscat:
        logger.critical(f'Cat_id {POSCAT_ID} not found!')

    questions: list[Question] = [que for que in (Question
         .select(Question, PosCat)
         .join(PosCat)
         .where(Question.poscat == poscat)
         .order_by(Question.description.asc())
         )]
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
                    text = f'<b>{answer.description}</b>' if answer.is_correct else answer.description
                    f.write(f'<li>{text}</li>')
                f.write('</ul>')
                f.write('<br>')
        f.write('</body>')
        f.write('</html>')
