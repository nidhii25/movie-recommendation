from fastapi import Query, HTTPException
from database import collection 
from fastapi import APIRouter

router = APIRouter()

@router.get("/genres")
async def get_genres():
    genres=await collection.distinct("genres")
    return genres

@router.get("/genres/{genre}/movies")
async def get_by_genre(genre:str,count:int=15):
    movies=[]
    cursor=collection.aggregate([{"$match":{"genres":genre}},{"$sample":{"size":count }}])
    async for movie in cursor:
        movie["_id"]=str(movie["_id"])
        movies.append(movie)
    return movies

@router.get("/genres/{genre}/movies/sort")
async def get_by_genre_sorted(genre:str,sort_by:str=Query(...,description="sort on basis of rating, release date, popularity, cast "),count:int=15):
    sort_field={
        "rating":"rating",
        "release_date":"release_date",
        "popularity":"popularity",
        "cast":"cast.0"
    }
    if sort_by not in sort_field:
        raise HTTPException(status_code=400,detail="Invalid sort_by value")
    movies = await collection.aggregate([
        {"$match": {"genres": genre}},
        {"$sample": {"size": count}}
    ]).to_list(length=count)

    for movie in movies:
        movie["_id"] = str(movie["_id"])
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found for the specified genre")
    return movies

