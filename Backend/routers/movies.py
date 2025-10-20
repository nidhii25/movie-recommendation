from fastapi import FastAPI
from database import collection 
from fastapi import APIRouter

router = APIRouter()

@router.get("/movies")
async def get_movies(count: int = 10): 
    movies= []
    cursor= collection.aggregate([{"$sample": {"size": count}}])
    async for document in cursor:
        document["_id"] = str(document["_id"])  
        movies.append(document)
    return movies

