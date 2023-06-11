from fastapi import FastAPI, APIRouter, Depends

from base_models.responses.base_response import BaseResponse
from models import Charts, SessionLocal, get_db

app = FastAPI()
song_router = APIRouter()

router = APIRouter(prefix="/v1/api")


@router.get("/charts", summary="returns all the charts", response_model=BaseResponse)
async def getCharts(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    charts = db.query(Charts) \
        .offset(skip).limit(limit) \
        .all()
    
    response_data = []
    for chart in charts:
        response_data.append(chart.response())
    
    response = BaseResponse(data={"artists": response_data})
    return response



@router.get("/charts/{chart_id}", response_model=BaseResponse,summary="Returns a specific chart by id")
async def getArticle(chart_id: int, db: SessionLocal = Depends(get_db)):
    chart = db.query(Charts).filter(Charts.id == chart_id).first()

    if chart is None:
        data = {"charts": []}
    else:
        data = {"chart": chart.response()}

    response = BaseResponse(data=data)
    return response
