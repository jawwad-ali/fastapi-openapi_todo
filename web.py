import requests
import streamlit as st

st.header("Todo App")

BASE_URL = "http://127.0.0.1:8000"  

# Get all todos 
def get_todos():
    response = requests.get(f"{BASE_URL}/")
    todos = response.json() 

    # Excluding the id field(from database) in the table
    modified_data = [{k: v for k, v in item.items() if k != 'id'} for item in todos]

    # Create a table with the modified data
    st.table(modified_data)
    return todos


# Create New Todo
def create_todo(): 
    title:str = st.text_input("Enter Todo Title")   
    description:str = st.text_area("Enter Todo Description")
      
    if st.button("Add Todo"):   
        response = requests.post(f"{BASE_URL}/create", json={"title": title , "description":description})
        st.title(response.reason)
        st.title(response.status_code)  
        if response.status_code == 200:  
            st.success("Todo added successfully")  
            # get_todos()  


if __name__ == "__main__":
    create_todo() 
    get_todos()