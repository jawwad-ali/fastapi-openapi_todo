from fastapi import FastAPI, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schema.types import UserModel, SystemUser

from auth.deps import get_current_user

from auth.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password  
)

from schema.types import User, Todo

from dbConnection import get_db

# initialzing fastapi object
app = FastAPI()
 
############################## Todo Endpoints ##############################

# add todo to databse
@app.post("/create")  
def create_todo(title: str = Body(..., embed=True), description: str = Body(..., embed=True) , db = Depends(get_db), user: UserModel = Depends(get_current_user)): 
    
    todo = Todo(title = title , description = description, user_email = user.email ) 
    
    db.add(todo)
    db.commit()   
    db.refresh(todo)

    return { 
        "title":title,
        "description":description,
        "user_id ":user.email
    } 







# getting current todo from db
@app.get("/") 
def get_todo(db = Depends(get_db) , user: UserModel = Depends(get_current_user)):
    todos_query = db.query(Todo).filter(user.email == Todo.user_email) 
    # db.refresh(todos_query) 
    return todos_query.all()








# Get todo which are completed(is_done = True)
# Updated Todo
@app.put("/update/{id}")
async def update_todo(
    id:int, 
    title:str = Body(..., embed=True), 
    description:str = Body(..., embed=True), 
    db = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    db_todo = db.query(Todo).filter(Todo.user_email == user.email , Todo.id == id).first()

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if title:  
        db_todo.title = title
        db_todo.description = description

    db.add(db_todo)  
    db.commit()
    db.refresh(db_todo)
    return title





# Delete Todo
@app.delete("/delete/{id}")
async def delete_todo(id:int , db = Depends(get_db), user: UserModel = Depends(get_current_user)):

    todo_query = db.query(Todo).filter(Todo.user_email == user.email , Todo.id == id).first()

    if todo_query is None:
        raise HTTPException(status_code=404, detail="Todo not found")  

    db.delete(todo_query)
    db.commit()  

    return {
        "message": "Todo deleted"
    }





############################## User Auth Endpoints ##############################

# Sign Up
@app.post("/signup" , summary = "Create New User")
def create_user(username:str = Body(... , embed=True), 
                email:str = Body(... , embed=True), 
                password:str = Body(... , embed=True), 
                db = Depends(get_db)): 
     
    #Password Hasing
    hashed_password = get_hashed_password(password)

    new_user = User( username=username, email=email, password=hashed_password)

    db.add(new_user)  
    db.commit()
    db.refresh(new_user)
    
    return {"message": "user created"}  
 
# Log In
@app.post("/login", summary="Login User")
def login(form_data: OAuth2PasswordRequestForm = Depends() , db = Depends(get_db)):
    
    # getting the username
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        ) 

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


# Get the info the current User
@app.get('/me', summary='Get details of currently logged in user')
def get_me(current_user: SystemUser = Depends(get_current_user), db = Depends(get_db) ):
    print(current_user)
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}