

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


def get_roadmaps():
    doc_ref = db.collection(u'roadmaps').get()
    docs = []
    for doc in doc_ref:
        docs.append(doc.to_dict())

    return docs


def get_roadmap(id: str):
    doc_ref = db.collection(u'roadmaps').document(id)
    return doc_ref.get().to_dict()