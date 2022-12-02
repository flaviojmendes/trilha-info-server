

from datetime import datetime
from os import environ
import uuid
from model.roadmap_view_model import RoadmapViewModel
from model.user_view_model import UserViewModel

from firebase_admin import firestore

from model.comment_model import CommentModel


db = firestore.client()


def create_comment(comment: CommentModel):

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



def get_comments(content_id: str):
    doc_ref = db.collection(u'comments').where(u'contentId', u'==', content_id).order_by(u"createdAt",  direction=firestore.Query.DESCENDING).get()
    docs = []
    for doc in doc_ref:
        docs.append(doc.to_dict())

    return docs

