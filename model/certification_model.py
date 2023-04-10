from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Answer(BaseModel):
    label: Optional[str]
    correct: Optional[bool]


class Question(BaseModel):
    description: Optional[str]
    answers: Optional[List[Answer]]
    selectedAnswer: Optional[Answer]


class Category(BaseModel):
    name: Optional[str]
    quantity: Optional[int]
    questions: Optional[List[Question]]


class Certification(BaseModel):
    id: Optional[str]
    title:   Optional[str]
    description: Optional[str]
    categories: Optional[List[Category]]


#  doc_ref.set({"nickname": nickname, "certificationId": certification_id,
#                 "correctQuestions": correct_questions, "questions": questions_dict, "title": certification['title']})
class CertificationResult(BaseModel):
    nickname: Optional[str]
    certificationId: Optional[str]
    correctQuestions: Optional[int]
    questions: Optional[List[Question]]
    title: Optional[str]
    date: Optional[datetime]
