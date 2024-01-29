import requests
import streamlit as st

import os  
from faker import Faker

fake = Faker()

# Generate fake user data


st.header("Todo App")

BASE_URL = "http://localhost:8000"  
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

USERTOKEN:str = None # Storing access token

# Initialize session state
if 'USERTOKEN' not in st.session_state:
    st.session_state["USERTOKEN"] = None

if "globalTitle" not in st.session_state:
    st.session_state["globalTitle"] = None

if "globalDescription" not in st.session_state:
    st.session_state["globalDescription"] = None

if "submitButton" not in st.session_state:
    st.session_state["submitButton"] = True

if 'df' not in st.session_state:
    st.session_state["df"] = None

placeholder = st.empty()  # Create an empty placeholder for the table

column_styles = """
<style>
    .column-style {
        background-color: purple;  
        padding: 15px;
        color:white;
        border-radius: 10px;
        margin: 10px;
    }

    .tabledata{
        background-color: black;
        color:white;
        padding:15px;
        margin:15px;
        border-radius: 10px;
    }

    .actionBtn {
        margin: 15px;
        padding:15px; 
        background-color: red;
        color: white;
        border: 1px solid white;
        border-radius: 10px;
    }

</style>
"""

def user_login(username, password):
    """
        User login functionality.
        Sending post request to login route.
    """

    global USERTOKEN  # Use the global keyword to modify the global variable
    response = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})

    # Checking if access token is there in json 
    if "access_token" in response.json():
        USERTOKEN = response.json()["access_token"]
        st.session_state["USERTOKEN"] = USERTOKEN

    return response.json() 

# Login 
def main():
    """
        Username and password are required to login. 
        If the user is logged in, then the todos are displayed. 
        If the user is not logged in, then the login page is displayed. 
        If the response contains an access token, then the user is logged in and the todos are displayed. 
    """
    if st.session_state["USERTOKEN"] is None:
        with placeholder.container(): 
            with st.form(key="login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                button = st.form_submit_button("Login")

                if button:
                    if username and password:  # Check if username and password are provided
                        user_login(username, password)
                        placeholder.empty()  # Clear the placeholder
                
                    else:
                        st.error("Username and password are required.")

# Get all todos 
def get_todos():
    """
        Getting todos for desired user.
    """

    if st.session_state["USERTOKEN"] is not None:  # Check if USERTOKEN is not None
        headers = {"Authorization": f"Bearer {st.session_state["USERTOKEN"]}"}
        response = requests.get(f"{BASE_URL}/", headers=headers) 

        if response.status_code == 200: 
            todos = response.json()

            # Show todo table 
            st.markdown(column_styles, unsafe_allow_html=True)

            colms = st.columns((1, 1, 1))
            fields = ["Title", "Description", "Action"]
            
            for col, field_name in zip(colms, fields):
                # Table Headers
                col.markdown(f'<div class="column-style">{field_name}</div>', unsafe_allow_html=True)
                col1, col2 = st.columns([2, 1])  # Adjust the ratio as needed

            for item in todos:
                #  Table Data
                col1, col2, col3 = st.columns((1, 1, 1 ))
 
                col1.markdown(f'<div class="tabledata">{item["title"]}</div>', unsafe_allow_html=True)
                col2.markdown(f'<div class="tabledata">{item["description"]}</div>', unsafe_allow_html=True)
                

                # # Delete button 
                do_action = col3.button("Delete",key=item["id"])

                if do_action:
                    # Delete Endpoint
                    response = requests.delete(f"{BASE_URL}/delete/{item["id"]}", headers=headers)
                    response.json()

                    if response.status_code == 200: 
                        st.error(f"{item["title"]} deleted")
            return todos 
    
        elif response.status_code == 401:
            st.error("Unauthorized. Please log in.")
        else: 
            st.error(f"Error fetching todos. Status code: {response.status_code}")
    else:
        st.error("Please log in to view todos.")

 

# Create New Todo
def create_todo(): 
    """
        Creating a new todo. 
        If the user is logged in, then the create todo form is displayed. 
        If the user is not logged in, then the login page is displayed. 
        If the create todo form is submitted, then the title and description are sent to the create route. 
        The todos are displayed in the table after the todo is added. 
        The create todo form is cleared after the todo is added. 
        The create todo form is displayed again after the todo is added. 
    """

    if st.session_state["USERTOKEN"] is not None: 
        headers = {"Authorization": f"Bearer {st.session_state["USERTOKEN"]}"}

        with st.form(key="create_todo_form"):
            title = st.text_input("Enter Todo Title", key="todo_title")
            description = st.text_input("Enter Todo Description", key="todo_description")

            st.session_state["globalTitle"] = title
            st.session_state["globalDescription"] = description

            submitted = st.form_submit_button("Add Todo") 
            
            st.session_state["submitButton"] = submitted

            if st.session_state["submitButton"] and st.session_state["globalTitle"] and st.session_state["globalDescription"]:
                response = requests.post(
                    f"{BASE_URL}/create",
                    json={
                        "title": st.session_state["globalTitle"], 
                        "description": st.session_state["globalDescription"]},
                    headers=headers 
                )

                if response.status_code == 200:
                    st.success("Todo added successfully")
                    st.session_state["globalTitle"] = None
                    st.session_state["globalDescription"] = None

    st.session_state["df"] = get_todos() 

if __name__ == "__main__":
    main()
    # get_todos()
    create_todo()   