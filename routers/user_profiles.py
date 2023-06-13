from fastapi import APIRouter, Depends
from helpers.logger import log

from base_models.responses.base_response import BaseResponse
from models import SessionLocal, get_db, UserProfiles

router = APIRouter(prefix="/v1/api")


@router.get("/user-profiles", summary="returns the user profiles of all registered users", response_model=BaseResponse)
async def userProfiles(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    userProfiles = db.query(UserProfiles) \
        .offset(skip).limit(limit) \
        .all()

    response_data = []
    for userProfile in userProfiles:
        response_data.append(userProfile.fixModelFieldsForResponse(False))

    response = BaseResponse(data={"user_profiles": response_data})
    return response

@router.get("/user-profiles/{user_profile_id}", summary="returns the user profile that matches the provided user profile id", response_model=BaseResponse)
async def userProfiles(user_profile_id: int, user_id: str = None, db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    userProfile = db.query(UserProfiles).filter(UserProfiles.id == user_profile_id).first()

    if userProfile is None:
        data = {"user_profile": None}
    else:
        data = {"user_profile": userProfile.fixModelFieldsForResponse(False)}

    response = BaseResponse(data=data)
    return response
