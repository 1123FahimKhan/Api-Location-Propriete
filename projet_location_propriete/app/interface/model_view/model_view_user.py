import datetime

from pydantic import BaseModel, ConfigDict

class UserView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    username: str
    email: str
    role: str
    created_at: datetime.datetime
