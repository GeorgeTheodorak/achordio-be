from fastapi import FastAPI, APIRouter

app = FastAPI()
song_router = APIRouter()


class ItemRouter:
    @song_router.get("/songs")
    async def get_items(self):
        return {"message": "Get all songs"}



item_router = ItemRouter()
app.include_router(song_router, tags=["items"], prefix="/api")