from pydantic import BaseModel, EmailStr

class Profile(BaseModel):
    user_id:int
    name:str
    description:str

class ProfileResponse(Profile):
    id_profile:int
    class Config:
        orm_mode = True

class User(BaseModel):
    name:EmailStr
    profiles: list[Profile]
    favoriteProfiles: list[Profile]

class UserResponse(User):
    user_id:int
    class Config:
        orm_mode = True