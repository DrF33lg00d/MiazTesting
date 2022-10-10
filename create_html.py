from db import db


if '__main__' == __name__:
    print('Create file')
    questions = db.get_all_questions()
    questions.sort(key=lambda x: x['description'])
    for question in questions:
        question['answers'] = db.get_all_answers(question['id'])
    with open('answers.html', 'w', encoding='cp1251') as f:
        f.write('<html>')
        f.write('<head>')
        f.write('<title>Answers</title>')
        f.write('</head>')

        f.write('<body>')
        for question in questions:
            f.write(f'<em>{question["description"]}</em><br>')
            f.write('<ul>')
            for answer in question['answers']:
                text = f'<b>{answer["description"]}</b>' if answer['is_correct'] else answer['description']
                f.write(f'<li>{text}</li>')
            f.write('</ul>')
            f.write('<br>')
        f.write('</body>')
        f.write('</html>')
