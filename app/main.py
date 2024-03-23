from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import requests
from pymongo.errors import ServerSelectionTimeoutError
import logging
import requests
import pytest

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb+srv://atharva22110116:j1db3hmyyaWorY4l@fastapiproject.gfmoy1c.mongodb.net/")
db = client["github_contributors"]
collection = db["FastAPIproject"]

class RepositoryInput(BaseModel):
    owner: str
    repo: str

class ContributorInfo(BaseModel):
    owner: str
    repo: str
    username: str
    type: str

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

def fetch_contributors(owner: str, repo: str) -> List[dict]:
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json()["message"])
    return response.json()


def store_contributors(contributors: List[dict]) -> int:
    result = collection.insert_many(contributors)
    return len(result.inserted_ids)

@app.get("/check-database-connection")
def check_database_connection():
    try:
        # Attempt to perform a simple database operation
        collection_count = collection.count_documents({})
        return {"message": f"Successfully connected to MongoDB. Collection count: {collection_count}"}
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")

@app.post("/ingest-contributors", response_model=dict)
def ingest_contributors(repo_input: RepositoryInput):
    contributors = fetch_contributors(repo_input.owner, repo_input.repo)
    num_contributors = store_contributors(contributors)
    return {"message": f"{num_contributors} contributors ingested successfully"}

@app.post("/get-contributor-info", response_model=dict)
def get_contributor_info(info: ContributorInfo):
    # Query MongoDB collection based on provided parameters
    contributor_data = collection.find_one({
        "owner": info.owner,
        "repo": info.repo,
        "username": info.username,
        "type": info.type
    })

    if not contributor_data:
        raise HTTPException(status_code=404, detail="Contributor not found")

    # Construct response payload
    response_data = {
        "username": contributor_data["username"],
        "avatar_url": contributor_data["avatar_url"],
        "site_admin": contributor_data["site_admin"],
        "contributions": contributor_data["contributions"]
    }
    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)