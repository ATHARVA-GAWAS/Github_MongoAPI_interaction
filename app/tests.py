# test_myapp.py

from fastapi import HTTPException
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, fetch_contributors, store_contributors

@pytest.fixture
def client():
    return TestClient(app)

def test_fetch_contributors_success():
    # Mocking the requests.get function to return a predefined response
    with patch("main.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"login": "user1", "contributions": 10}, {"login": "user2", "contributions": 5}]
        
        contributors = fetch_contributors("owner", "repo")
        
        assert contributors == [{"login": "user1", "contributions": 10}, {"login": "user2", "contributions": 5}]

def test_fetch_contributors_failure():
    # Mocking the requests.get function to return a predefined error response
    with patch("main.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"message": "Not Found"}
        
        with pytest.raises(HTTPException) as exc_info:
            fetch_contributors("owner", "repo")
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Not Found"

def test_store_contributors():
    # Mocking the MongoDB collection.insert_many function to return a predefined result
    with patch("main.collection.insert_many") as mock_insert_many:
        mock_insert_many.return_value.inserted_ids = [1, 2, 3]
        
        num_contributors = store_contributors([{"login": "user1", "contributions": 10}, {"login": "user2", "contributions": 5}])
        
        assert num_contributors == 3
