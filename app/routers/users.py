from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model = list[schemas.UserResponse])
async def view_users(db: Session = Depends(get_db)):
    users = db.query( models.User ).all()
    return users

@router.get("/{userName}", response_model = schemas.UserResponse)
async def view_user(userName:str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == userName).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user {userName} not found")

    return user

@router.put("/{userName}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(updateUser:schemas.User, userName:str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == userName)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user {userName} not found")
    user.update(updateUser.model_dump(), synchronize_session=False)
    db.commit()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserResponse)
async def add_user(aUser:schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**aUser.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@router.delete("/{userName}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(userName:str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == userName)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user {userName} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)