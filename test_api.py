from fastapi.testclient import TestClient
from fastapi import Depends 

from main import app

from dbConnection import get_db 

client = TestClient(app)

# JWT TOKEN OF THE USER. Change this token after every 30 mins because of expiry.
valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDU5NDIxMjcsInN1YiI6ImFsaUBnbWFpbC5jb20ifQ.DwvqeHTVBHZaINaujDG-c1k5SGvD42CYuDuS-eng5tg"
 
# test to add a todo
def test_add_todo( response = Depends(get_db) ): 
    response = client.post("/create/", json={"title": "test todo" , "description": "test description"},headers={
        "Authorization": f"Bearer {valid_token}"
    })
    assert response.status_code == 200 
    assert response.json()["title"] == "test todo"  
    # db.close() 
 
# Test to delete a todo
def test_delete_todo(response = Depends(get_db)):
    response = client.delete("/delete/6", 
        headers={"Authorization": f"Bearer {valid_token}"}) 
    
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted"  
    # db.close()

# Test to update a todo
# def test_update_todo(response = Depends(get_db)):
#     response = client.put("/update/26", json={"title": "Updated Todo", "description": "Updated Description"})
#     assert response.status_code == 200
#     assert response.json() == "Updated Todo"  

# User Sign Up
# def test_signup():
#     response = client.post("/signup", json={"username": "hiba", "email": "hiba@gmail.com", "password": "123"})
#     assert response.status_code == 200  # Adjust this line based on the actual status code
#     assert response.json() == {"message": "user created"}