from fastapi import Response,status,Depends,APIRouter,HTTPException
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List,Optional

router=APIRouter(
    prefix="/vote",
    tags=['votes'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_vote(vote:schemas.Vote,db: Session = Depends(get_db),
                            user: int= Depends(oauth2.get_current_user)):

    #new_post=models.Post(title=post.title,content=post.content,published=post.published)
    post_query=db.query(models.Post).filter(models.Post.id==vote.post_id)
    found_post=post_query.first()
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id ,models.Vote.user_id==int(user.id_tokendata))
    found_vote=vote_query.first()

    if(found_post is None) :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this post does not exist")
    else :
        if(vote.dir==1 ): 
            if found_vote :
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you have already liked this post")
            else :
                new_vote=models.Vote(post_id=vote.post_id,user_id=user.id_tokendata)#it matches the fields automatically
                db.add(new_vote)
                db.commit()
                db.refresh(new_vote)
                return {"message":"vote added successfully "}
        else : 
            vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)