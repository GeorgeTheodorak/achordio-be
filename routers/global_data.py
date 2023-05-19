from fastapi import APIRouter

router = APIRouter(prefix="/v1/api")


@router.get("/global-data", summary="returns constants and important data")
async def globalData():
    return {
        "data": {
            "error_codes": {
                "no_auth": 1,
                "bad_request": 2
            }
        }
    }
