from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/profiles",
    tags=["Profile"]
)

@router.get("/", response_model = list[schemas.ProfileResponse])
async def view_profiles(db: Session = Depends(get_db)):
    profiles = db.query( models.Juego ).all()
    return profiles

@router.get("/{profile_id}", response_model = schemas.ProfileResponse)
async def view_profile(profile_id:int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.profile_id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the profile {profile_id} not found")
    return profile

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ProfileResponse)
async def add_profile(aProfile:schemas.Profile, db: Session = Depends(get_db)):
    new_profile = models.Profile(**aProfile.model_dump())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.put("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(updateProfile:schemas.Profile, profile_id:int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.profile_id == profile_id)
    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the profile {profile_id} not found")
    profile.update(updateProfile.model_dump(), synchronize_session=False)
    db.commit()

@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id:int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.profile_id == profile_id)
    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the profile {profile_id} not found")
    profile.delete(synchronize_session=False)
    db.commit()