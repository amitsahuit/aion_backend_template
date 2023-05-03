from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    company_id: int
    projects_handled: Optional[List[str]] = ["vodafone", "airtel", "idea"]
    phone_number: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    address: Optional[str] = None
    married_status: Optional[bool] = False
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "amit",
                "email": "amit@hcl.com",
                "age": 27,
                "company_id": 52155651,
                "projects_handled": ["vodafone", "airtel", "idea"],
                "address": "Bengalore",
                "Phone_number": 8197920447,
            }
        }
