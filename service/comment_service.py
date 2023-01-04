

from datetime import datetime
from os import environ
import uuid
from model.roadmap_view_model import LevelViewModel, RoadmapViewModel
from model.user_view_model import UserViewModel

from firebase_admin import firestore
from mdutils.mdutils import MdUtils
from mdutils import Html
from typing import List
from model.note_model import NoteModel
from firebase_admin import credentials
from firebase_admin import initialize_app

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"
cred = credentials.ApplicationDefault()
initialize_app(cred, {
    'projectId': "trilha-info",
})


db = firestore.client()


def create_comment(comment: NoteModel):

    if comment.id is None:
        comment.id = str(uuid.uuid4())

    doc_ref = db.collection(u'comments').document(comment.id)

    commentDict = comment.dict()

    doc_ref.set(commentDict)

    return comment


def remove_comment(comment_id: str, user_name: str):
    doc_ref = db.collection(u'comments').document(comment_id)
    doc_owner = doc_ref.get().to_dict()['author']
    if user_name == doc_owner:
        db.collection(u'comments').document(comment_id).delete()



def get_comments(content_id: str, nickname: str):
    doc_ref = db.collection(u'comments').where(u'contentId', u'==', content_id).where(u'author', u'==', nickname).order_by(u"createdAt",  direction=firestore.Query.DESCENDING).get()
    docs = []
    for doc in doc_ref:
        docs.append(doc.to_dict())

    return docs

def export_comments_markdown(nickname: str):
    doc_ref = db.collection(u'comments').where(u'author', u'==', nickname).order_by(u"createdAt",  direction=firestore.Query.DESCENDING).get()
    
    mdFile = MdUtils(file_name='TrilhaInfo_Notes', title='Anotações Trilha Info', author=nickname)
    mdFile.new_header(level=1, title="")
    categories = {}

    for doc in doc_ref:
        doc_dict = doc.to_dict()
        
        if doc_dict['contentId'] not in categories:
            categories[doc_dict['contentId']] = [doc_dict]
        else:
            categories[doc_dict['contentId']].append(doc_dict)

    for key in categories.keys():
        mdFile.new_line()
        mdFile.new_header(level=2, title=key)
        for note in categories[key]:
            note_text = note['createdAt'].strftime("%m/%d/%Y %H:%M") + " - " + note['text']
            mdFile.new_paragraph(text=note_text)

    return mdFile.get_md_text()

