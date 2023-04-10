
import time
from typing import List
import uuid
from model.certification_model import Certification, CertificationResult, Question
from firebase_admin import firestore

db = firestore.client()

html_certification = {
    "title": 'Certificação HTML',
    "description": 'Teste seus conhecimentos em HTML e obtenha sua certificação da Trilha Info.',

    "categories": [
        {
            "name": 'HTML Básico',
            "quantity": 4,
            "questions": [
                {
                    "description": 'O que é HTML?',
                    "answers": [
                        {
                            "label":
                            'HTML é uma linguagem de marcação que tem o objetivo de estruturar e organizar o conteúdo da página.',
                            "correct": True,
                        },
                        {"label": 'HTML é um personagem da turma da mônica.',
                         "correct": False},
                        {"label": 'HTML é uma marca de bicicleta. ', "correct": False},
                    ],
                },
                {
                    "description": 'O HTML pode ser considerado uma linguagem de programação?',
                    "answers": [
                        {"label": 'Sim', "correct": False},
                        {"label": 'Não', "correct": True},
                    ],
                },
                {
                    "description": 'Qual destas tag não é uma tag HTML?',
                    "answers": [
                        {"label": '<head>', "correct": False},
                        {"label": '<body>', "correct": False},
                        {"label": '<ear>', "correct": True},
                        {"label": '<footer>', "correct": False},
                    ],
                },

                {
                    "description": 'Qual o significado da sigla HTML?',
                    "answers": [
                        {"label": 'Hipopótamos Tem Muito Leite', "correct": False},
                        {"label": 'Hypertext Markup Language', "correct": True},
                        {"label": 'Helicópteros Tomahawk Marrons Leves',
                            "correct": False},
                    ],
                },
            ],
        },
    ],
}


def get_certification(id: str):

    doc_ref = db.collection(u'certifications').document(id)
    certification = doc_ref.get().to_dict()

    for category in certification['categories']:
        for question in category['questions']:
            for answer in question['answers']:
                answer['correct'] = None

    return certification


def validate_certification(questions: List[Question], id: str, nickname: str):
    correct_questions = 0
    for question in questions:
        for category in html_certification['categories']:
            for q in category['questions']:
                if q['description'] == question.dict()['description']:
                    for answer in q['answers']:
                        if answer['correct'] == True:
                            if answer['label'] == question.dict()['selectedAnswer']['label']:
                                correct_questions += 1
                                question.selectedAnswer.correct = True
                                break

    certification_id = save_certification(
        nickname, id, correct_questions, questions)

    return certification_id


def save_certification(nickname: str, certification_id: str, correct_questions: int, questions: List[Question]):
    certification_result_id = str(
        uuid.uuid5(uuid.NAMESPACE_DNS, nickname + str(time.time())))

    doc_ref = db.collection(
        u'certification-results').document(certification_result_id)

    questions_dict = []
    for question in questions:
        questions_dict.append(question.dict())

    certification_doc_ref = db.collection(u'certifications').document(
        certification_id)

    certification = certification_doc_ref.get().to_dict()

    certification_result = CertificationResult()
    certification_result.nickname = nickname
    certification_result.certificationId = certification_id
    certification_result.correctQuestions = correct_questions
    certification_result.questions = questions_dict
    certification_result.title = certification['title']
    certification_result.date = time.time()

    doc_ref.set(certification_result.dict())

    return certification_result_id


def get_certification_result(certification_result_id: str, nickname: str):

    doc_ref = db.collection(
        u'certification-results').document(certification_result_id)

    certification_result = doc_ref.get().to_dict()

    if certification_result['nickname'] != nickname:
        raise Exception("Certification does not belong to this user.")

    return certification_result


def get_certification_results(nickname: str):

    doc_ref = db.collection(u'certification-results').where(
        u'nickname', u'==', nickname).get()
    docs = []
    for doc in doc_ref:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        docs.append(doc_dict)

    return docs


def get_certification_highest_score(certification_id: str, nickname: str):
    doc_ref = db.collection(u'certification-results').where(
        u'nickname', u'==', nickname).where(u'certificationId', u'==', certification_id).order_by(u'correctQuestions', direction=firestore.Query.DESCENDING).limit(1).get()

    for doc in doc_ref:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        return doc_dict

    return None