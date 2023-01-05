from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel


class LinkType(Enum):
    FREE = 'Grátis'
    PAID = 'Pago'


class LinkContentType(Enum):
    WATCH = "Assista"
    READ = "Leia"
    LISTEN = "Ouça"
    VISIT = "Visite"
    PRACTICE = "Pratique"

class LinkViewModel(BaseModel):
    url: str
    type: Optional[str]
    votes: Optional[int]
    contentType: LinkContentType
    label: str


class RoadmapItemViewModel(BaseModel):
    label: str
    description: Optional[str]
    children: Optional[List['RoadmapItemViewModel']]
    links: Optional[List[LinkViewModel]]


class LevelViewModel(BaseModel):
    label: Optional[str]
    description: Optional[str]
    items: List[RoadmapItemViewModel]


class RoadmapViewModel(BaseModel):
    id: Optional[str]
    title: Optional[str]
    owner: Optional[str]
    description: Optional[str]
    slug: Optional[str]
    levels: List[LevelViewModel]
