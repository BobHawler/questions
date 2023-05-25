from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/questions_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Questions(db.Model):
    __tablename__ = 'questions_db'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=True)
    question = db.Column(db.String(300))
    answer = db.Column(db.String(300))
    date = db.Column(db.DateTime)

    def __init__(self, question_id: int, question: str, answer: str, date: str) -> None:
        self.question_id = question_id
        self.question = question
        self.answer = answer
        self.date = date

    def __repr__(self) -> str:
        return f'Question id {self.question_id}'


@app.route('/', methods=['POST'])
def add_questions() -> dict:
    questions_num = request.json["questions_num"]

    response = requests.get(f'https://jservice.io/api/random?count={questions_num}')
    questions = response.json()

    for i in range(questions_num):
        unit = questions[i]
        check_id = Questions.query.filter_by(question_id=unit['id']).count()
        while check_id > 0:
            response = requests.get('https://jservice.io/api/random?count=1')
            unit = response.json()
            check_id = Questions.query.filter_by(question_id=unit['id']).count()
        get_new_question = Questions(
                                     question_id=unit['id'],
                                     question=unit['question'],
                                     answer=unit['answer'],
                                     date=unit['created_at'])
        db.session.add(get_new_question)
        db.session.commit()

    last_question = Questions.query.order_by(Questions.id.desc()).limit(1).all()
    if last_question:
        question = last_question[0]
    else:
        question = Questions()
    return jsonify({
        "question_id": question.question_id,
        "question": question.question,
        "answer": question.answer,
        "date": question.date
    })


if __name__ == '__main__':
    app.run()
