from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    skills: List[str] = Field(default=[])
    projects_created: List[str] = Field(default=[])
    projects_participating: List[str] = Field(default=[])
    availability: Optional[str] = Field(default="")
    interests: List[str] = Field(default=[])
    orcid_id: Optional[str] = Field(default="")
    communications: List[str] = Field(default=[])
    privacy_preference: bool = Field(default=True)

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@scicollab.com",
                "password": "securepassword",
                "skills": ["Python", "FastAPI"],
                "projects_created": ["Project1"],
                "projects_participating": ["Project2"],
                "availability": "Weekdays after 6pm",
                "interests": ["API Development", "Machine Learning"],
                "orcid_id": "0000-0001-1234-5678",
                "communications": ["Conversation1"],
                "privacy_preference": True,
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    skills: Optional[List[str]]
    projects_created: Optional[List[str]]
    projects_participating: Optional[List[str]]
    availability: Optional[str]
    interests: Optional[List[str]]
    orcid_id: Optional[str]
    communications: Optional[List[str]]
    privacy_preference: Optional[bool]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
