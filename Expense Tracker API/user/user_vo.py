from pydantic import BaseModel, EmailStr

class UserRequst(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str