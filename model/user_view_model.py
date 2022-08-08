from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserViewModel(BaseModel):
    user_login: str
    creation: Optional[datetime]
    last_login: Optional[datetime]