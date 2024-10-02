from fastapi import FastAPI,Response,status,Depends
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
#you can see the documentation of the api by searching
#url/docs or url/redoc,example http..1008:8000/docs or 
from . import models,schemas,utils
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Optional,List


models.Base.metadata.create_all(bind=engine)


app = FastAPI()





conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Roua+affes2021',
                      cursor_factory=RealDictCursor)

cursor=conn.cursor()

print("bonjour")
#we call this code below a path operation  or a route 
@app.get("/")#we call this a decorator to the function bellow 
def root():
    return {"message": "Hello Roua Affes"}

@app.get("/posts/sqlalchemy",response_model=List[schemas.ResponsePost])#we call this a decorator to the function bellow 
def test_posts(db: Session = Depends(get_db)):

    posts=db.query(models.Post).all()
    return posts

# when afficher les return it takes the first match so if i have two function with
#  @app.get("/") it will apply the first one 

my_posts=[{"title":"hi","content":"conteneeuh","id":1},
          {"title":"bonsoir","content":"bienvenue à paris","id":2}]
@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts=cursor.fetchall()
    return posts




#even though the POST method is used to send data, the server can still retrieve that data 
# from the request body using FastAPI's Body(...) utility. 
# The key difference is that the data is not retrieved from a database or another source, 
# but directly from what the client sent as part of the request.

# we retrieve the data as a dictionary and put it in the payload variable 
#@app.post("/createposts")

#def create_posts(payLoad: dict = Body(...)):
#    print(payLoad)
#    return{"new post":f"title {payLoad['title']} content {payLoad['content']}"}

# we want postst to have certain elements like title and content 
# to do that we use the pydantric library to define the elements we want 
#it's like a contract 

#title str ,content str 

     
@app.post("/posts")

def create_posts(post:schemas.PostCreate):
    #print(post)
    #you can convert the new_post variable from a pydantic model to a dictionary
    #print(post.model_dump()) #here we convert new_post from pydantric model to dictionary
    #mise à jour use .model_dump() instead of .dict()
    #post_dict=post.model_dump()
    #post_dict['id']=randrange(0,1000000)#we want each post to be unique 
    #my_posts.append(post_dict)#adding new post to the already existing ones
    #return{"data ":post_dict}
    #When returned in a FastAPI endpoint, FastAPI will automatically convert the new_post 
    # object to JSON. If new_post is still a Pydantic model at this point, 
    # FastAPI will use the model’s data to generate a JSON response.

    cursor.execute("""insert into posts(title,content_post,published) values(%s,%s,%s) returning * """,
                  (post.title,post.content,post.published)) 
    
    #The RETURNING * clause in your SQL INSERT statement is used to return the data 
    # of the newly inserted row immediately after the insert operation.
    #  This is particularly useful when you want to know what was inserted, 
    # especially if the database generates values (like auto-incremented IDs) that you may want to use or confirm.
    new_post=cursor.fetchone()
    conn.commit()
    return new_post

@app.post("/posts/sqlalchemy",response_model=schemas.ResponsePost)

def create_posts_sqlalchemy(post:schemas.PostCreate,db: Session = Depends(get_db)):

    #new_post=models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(**post.model_dump())#it matches the fields automatically
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def find_post(id):
    for post in my_posts:
        if post["id"]==id:
            return post
        


@app.get("/posts/{id}",response_model=schemas.ResponsePost)#the id here is a path parameter and is always retrieved as a string 
def get_post(id:int,response:Response):#id:int convert the id to number and give good message error if the id is not a number 
    #post=find_post(id) 
    #if id not found we want to have the 404 not found status code in postman and not 200ok so 
    cursor.execute("""select * from posts where id_post=%s""",(str(id),))
    post=cursor.fetchone()
    if not post :
        response.status_code =404
        #or
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message":"post not found"}
    else :
        return post

@app.get("/posts/sqlalchemy/{id}",response_model=schemas.ResponsePost )#the id here is a path parameter and is always retrieved as a string 
def get_post(id:int,response:Response,db: Session = Depends(get_db)):#id:int convert the id to number and give good message error if the id is not a number 
    #post=find_post(id) 
    #if id not found we want to have the 404 not found status code in postman and not 200ok so 
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    else :
        return post

def find_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id :
            return i 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #index = find_index(id)
    cursor.execute("""select * from posts where id_post=%s""",(str(id),))
    index=cursor.fetchone()
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    else:
        #my_posts.pop(index)
        cursor.execute("""delete from posts where id_post=%s""",(str(id),))
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts/sqlalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    else:
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate):
    #index = find_index(id)
    cursor.execute("""select * from posts where id_post=%s """,(str(id),))
    index=cursor.fetchone()
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    
    #create new dictionary
    #post_dict = updated_post.model_dump()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    #return {"data": updated_post.model_dump()}
    else :
        cursor.execute("""update posts set title=%s, content_post=%s where id_post=%s returning * """,
                       (updated_post.title, updated_post.content, str(id)))
        conn.commit()
        return cursor.fetchone()

@app.put("/posts/sqlalchemy/{id}",response_model=schemas.ResponsePost)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    #index = find_index(id)
    
    post_query=db.query(models.Post).filter(models.Post.id==id)    
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    

    else :
        post_query.update(updated_post.model_dump())
        db.commit()
        return post_query.first()
    


#-------------------USERS---------------------------------------------------------------


@app.post("/users/sqlalchemy",response_model=schemas.UserResponse)

def create_posts_sqlalchemy(user:schemas.UserCreate,db: Session = Depends(get_db)):

    hashed_password=utils.hash_password(user.password)
    user.password=hashed_password

    new_user=models.Users(**user.model_dump())#it matches the fields automatically
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/sqlalchemy/{id}",response_model=schemas.UserResponse )#the id here is a path parameter and is always retrieved as a string 
def get_user(id:int,response:Response,db: Session = Depends(get_db)):#id:int convert the id to number and give good message error if the id is not a number 
    #post=find_post(id) 
    #if id not found we want to have the 404 not found status code in postman and not 200ok so 
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not exist")
    else :
        return user