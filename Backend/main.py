from fastapi import FastAPI
from database import collection
from routers import movies, genres,recommendation

app= FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Recommendation API"}

app.include_router(movies.router)
app.include_router(genres.router)
app.include_router(recommendation.router)