from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel


class NoteModel(BaseModel):
    id: Optional[str]
    text: Optional[str]
    author: Optional[str]
    createdAt: Optional[datetime]
    contentId: Optional[str]
