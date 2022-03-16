from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

people = MongoClient("mongodb+srv://admin:BDVoTAlwXkMtaSqk@cluster0.vw4xy.mongodb.net/test")["examples"]["people"]

app = FastAPI()

class person(BaseModel):
    name: str
    age: int
    gender: str

def personWithId(db_item):
    return{
        "_id": str(db_item["_id"]),
        "name": db_item["name"],
        "age": db_item["age"],
        "gender": db_item["gender"]
    }

@app.post("/person")
async def addReprimand(pers: person):
    """Used to add a person to the database"""
    result = people.insert_one(pers.dict())
    return { "insertion" : result.acknowledged }

@app.get("/people")
async def main():
    """Gets all people from the database"""
    list = people.find()
    return [personWithId(item) for item in list]