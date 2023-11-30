from pydantic import BaseModel


class UserRegistration(BaseModel):
    FIO: str
    username: str
    password: str
    email: str
    isAdmin: bool
    isTeacher: bool
    isCurator: bool

class UserLogin(BaseModel):
    FIO: str
    username: str
    password: str
    email: str



class TokenData(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
