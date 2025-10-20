from fastapi import Query, HTTPException
from database import collection 
from fastapi import APIRouter
from models import recomm_ques
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

@router.post("/recommendations")
async def get_choice(ques: recomm_ques):
    genre = ques.genre
    min_ratings = ques.min_ratings
    fav_movie = ques.fav_movie

    fav = await collection.find_one({"title": fav_movie})
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite movie not found")
    fav_overview = fav.get("overview", "")
    cursor = collection.find({
        "genres": genre,
        "vote_average": {"$gte": min_ratings},
        "title": {"$ne": fav_movie}
    }).limit(100)  

    movies_list = await cursor.to_list(length=100)
    if not movies_list:
        return {"recommended_movies": []}

    overviews = [movie.get("overview", "") for movie in movies_list]
    all_overviews = [fav_overview] + overviews

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(all_overviews)

    fav_vector = tfidf_matrix.getrow(0)  
    other_vectors = [tfidf_matrix.getrow(i) for i in range(1, tfidf_matrix.shape[0])]

    cos_scores = np.array([cosine_similarity(fav_vector, row)[0][0] for row in other_vectors])

    top_indices = cos_scores.argsort()[::-1][:10]  

    recommended_movies = [movies_list[i] for i in top_indices]

    for movie in recommended_movies:
        movie["_id"] = str(movie["_id"])

    return {"recommended_movies": recommended_movies}
