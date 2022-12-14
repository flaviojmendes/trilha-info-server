

from datetime import datetime
from os import environ
from model.user_view_model import UserViewModel
from firebase_admin import firestore



db = firestore.client()


def create_user(user: UserViewModel):
    doc_ref = db.collection(u'users').document(user.user_login)
    doc_ref.set({
        u'user_login': user.user_login,
        u'creation': datetime.now(),
        u'last_login': datetime.now()
    })

    return True

def update_user(user: UserViewModel):
    doc_ref = db.collection(u'users').document(user.user_login)
    doc_ref.set({
        u'last_login': datetime.now()
    })

    return True


def get_user(user_login: str):
    doc_ref = db.collection(u'users').document(user_login)
    if doc_ref.get().exists:
        return doc_ref.get().to_dict()
    raise Exception("User does not exist")