from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SchUserRegister(BaseModel):
    email: EmailStr
    password: str


class SchUserLogin(BaseModel):
    email: EmailStr = Field(examples=['Pavel@example.com'])
    password: str = Field(examples=['Pavel'])

    model_config = ConfigDict(from_attributes=True)


class SchGetUser(BaseModel):
    id: int
    email: str
