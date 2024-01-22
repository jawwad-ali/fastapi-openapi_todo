import requests
import streamlit as st

from jose import jwt

import os
import time

st.header("Todo App")

BASE_URL = "http://localhost:8000"  

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # should be kept secret
USERTOKEN:str = None

def user_login(username, password):
    global USERTOKEN  # Use the global keyword to modify the global variable
    response = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})

    # Checking if access token is there in json 
    if "access_token" in response.json():
        USERTOKEN = response.json()["access_token"]
        st.success("Login successful!")

    return response.json() 

# Login 
def main():
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:  # Check if username and password are provided
            user_login(username, password)

        else:
            st.error("Username and password are required.")

# Get all todos 
def get_todos():
    global USERTOKEN

    if USERTOKEN is not None:  # Check if USERTOKEN is not None
        headers = {"Authorization": f"Bearer {USERTOKEN}"}

        response = requests.get(f"{BASE_URL}/", headers=headers)

        st.write(response.status_code)
        
        if response.status_code == 200: 
            todos = response.json()
            # Excluding the id field (from database) in the table
            modified_data = [{k: v for k, v in item.items() if k != 'id'} for item in todos]

            # Create a table with the modified data
            st.table(modified_data)
            return todos 
        elif response.status_code == 401:
            st.error("Unauthorized. Please log in.")
        else:
            st.error(f"Error fetching todos. Status code: {response.status_code}")
    else:
        st.error("Please log in to view todos.")

# Create New Todo
# def create_todo(): 
#     title:str = st.text_input("Enter Todo Title")   
#     description:str = st.text_area("Enter Todo Description")
      
#     if st.button("Add Todo"):   
#         response = requests.post(f"{BASE_URL}/create", json={"title": title , "description":description})
#         st.title(response.reason)
#         st.title(response.status_code)  
#         if response.status_code == 200:  
#             st.success("Todo added successfully")  


if __name__ == "__main__":
    main()
    get_todos()
    # create_todo() 

    # if auth():
    #     page()
    # else:
    #     st.write("UnAuth")