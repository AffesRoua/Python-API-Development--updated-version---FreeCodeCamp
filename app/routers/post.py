from fastapi import Response,status,Depends,APIRouter,HTTPException
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func 

router=APIRouter(
    prefix="/posts/sqlalchemy",
    tags=['posts'])

@router.get("/",response_model=List[schemas.Post_vote])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search_title: Optional[str] = ""):
    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).filter(
        models.Post.title.contains(search_title)
    ).outerjoin(
        models.Vote, models.Post.id == models.Vote.post_id
    ).group_by(models.Post.id).limit(limit).offset(skip).all()


    posts=db.query(models.Post).filter(models.Post.title.contains(search_title)).limit(limit).offset(skip).all()

    return result



@router.post("/",response_model=schemas.ResponsePost)
def create_posts_sqlalchemy(post:schemas.PostCreate,db: Session = Depends(get_db),
                            user: int= Depends(oauth2.get_current_user)):

    #new_post=models.Post(title=post.title,content=post.content,published=post.published)
    print(user.id_tokendata)
    new_post=models.Post(owner_id=user.id_tokendata,**post.model_dump())#it matches the fields automatically
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



        


@router.get("/{id}",response_model=schemas.Post_vote )#the id here is a path parameter and is always retrieved as a string 
def get_post(id:int,response:Response,db: Session = Depends(get_db),user_id: int= Depends(oauth2.get_current_user)):#id:int convert the id to number and give good message error if the id is not a number 

    #result=db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).filter(
        models.Post.id==id
    ).outerjoin(
        models.Vote, models.Post.id == models.Vote.post_id
    ).group_by(models.Post.id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    else :
        return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),user_id: int= Depends(oauth2.get_current_user)):
    print(user_id)
    post_query=db.query(models.Post).filter(models.Post.id==id)

    if (post_query.first() is None)  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    
    elif (user_id.id_tokendata!=id) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this is not your post")
    
    else:
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}",response_model=schemas.ResponsePost)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db),user_id: int= Depends(oauth2.get_current_user)):
    
    
    
    post_query=db.query(models.Post).filter(models.Post.id==id)    
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist")
    

    elif (int(user_id.id_tokendata)!=post_query.first().owner_id) :
        print(type(user_id.id_tokendata))
        print(type(post_query.first().owner_id))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this is not your post")
    
    else :
        post_query.update(updated_post.model_dump())
        db.commit()
        return post_query.first()