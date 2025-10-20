from motor.motor_asyncio import AsyncIOMotorClient

client= AsyncIOMotorClient("mongodb://localhost:27017")
db=client["movie_db"]
collection=db["movies"]