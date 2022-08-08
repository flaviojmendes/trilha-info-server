

from datetime import datetime
from os import environ
import uuid
from model.roadmap_view_model import RoadmapViewModel
from model.user_view_model import UserViewModel
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import initialize_app

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"
cred = credentials.ApplicationDefault()

initialize_app(cred, {
    'projectId': "trilha-info",
})

db = firestore.client()


def create_roadmap(roadmap: RoadmapViewModel):

    if roadmap.id is None:
        roadmap.id = str(uuid.uuid4())

    doc_ref = db.collection(u'roadmaps').document(roadmap.id)

    roadmapDict = roadmap.dict()

    for level in roadmapDict['levels']:
        if level['items']:
            for item in level['items']:
                if item['children']:
                    for section in item['children']:
                        if section['links']:
                            for link in section['links']:
                                link['contentType'] = link['contentType'].value

    doc_ref.set(roadmapDict)

    return roadmap


def remove_roadmap(roadmap_id: str, user_name: str):
    doc_ref = db.collection(u'roadmaps').document(roadmap_id)
    doc_owner = doc_ref.get().to_dict()['owner']
    if user_name == doc_owner:
        db.collection(u'roadmaps').document(roadmap_id).delete()



def get_roadmaps(user_login):
    doc_ref = db.collection(u'roadmaps').where(u'owner', u'==', user_login).get()
    docs = []
    for doc in doc_ref:
        docs.append(doc.to_dict())

    return docs


def get_roadmap(id: str):
    doc_ref = db.collection(u'roadmaps').document(id)
    return doc_ref.get().to_dict()