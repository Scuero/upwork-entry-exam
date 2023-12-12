from pydantic import BaseModel, EmailStr, Field

class Profile(BaseModel):
    name:str
    description:str

class ProfileResponse(Profile):
    user_id:int = Field(default=None)
    id_profile:int
    class Config:
        orm_mode = True

class User(BaseModel):
    name:EmailStr
    profiles: list[Profile] = Field(default=None)
    favoriteProfiles: list[Profile] = Field(default=None)

class UserResponse(User):
    user_id:int
    class Config:
        orm_mode = True