from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    gender: str
    ethnicity: str
    age: int

class LoginRequest(BaseModel):
    enrollment: str
    password: str

class AddRoleRequest(BaseModel):
    id_user: str
    role: str
