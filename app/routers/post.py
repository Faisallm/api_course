from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response, APIRouter
from .. import database, models, utils, schemas, oauth2
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    # for grouping of API's
    tags=['Posts'],
)

# order does matter.
my_posts = [
    {
        "id": 1,
        "title": "Gizo",
        "content": "Delivery to Mars."
    },
    {
        "id": 2,
        "title": "Pupa",
        "content": "Craiglist on Telegram."
    },
    {
        "id": 3,
        "title": "Kakaki",
        "content": "Jobs and Scholarships search engine."
    },
    {
        "id": 4,
        "title": "Imittis",
        "content": "Research AI."
    },
]

def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id: int):
   for index, p in enumerate(my_posts):
        if p['id'] == id:
            return index 

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 100,
              skip: int = 0,
              search: Optional[str] = ""):
    # filtering posts using a particular limit and skip...
    # with a conditional search query
    # this allows us to implement pagination from the frontend.
    print(search)
    all_posts = db.query(models.Post).filter(models.Post.title.contains(search)) \
        .limit(limit).offset(skip).all()

    # by default sqlalchemy performs a left inner join
    # we need an outer join
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)) \
        .limit(limit).offset(skip).all()

    # print(results)
    # print(all_posts)

    return all_posts

# user needs to be logged in to...
# get individual post.
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(database.get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    
    # filter post by id and get the first one (if multiples exist).
    # get the first entry.
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        # when post is not found in our db.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id: {id} does not exist!.")
    
    return post


# changing the default status code of a fastapi function.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    # the ** is for unpacking dictionary
    # model_dump() is preferred over dict()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    # same as returning *
    db.refresh(new_post)

    return new_post

# user needs to be logged-in to delete.
# we don't send any data back in a delete function.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # get the first entry
    # the reason why we don't add .first() is because...
    # we want to delete the post
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        # when post is not found in our db.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id: {id} does not exist!.")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    
    # deleting post from db
    post.delete(synchronize_session=False)
    # make permanent changes to db.
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    # retrieve the post index to be updated.
    post_query = db.query(models.Post).filter(models.Post.id == id)
    

    if not post_query.first():
        # when post is not found in our db.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id: {id} does not exist!.")
    
    # to ensure that the current user owns the post.
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")

    # there is no need for unpacking while updating.
    post_query.update(post.model_dump(), synchronize_session=False)
    # make permanent changes to db
    db.commit()
    
    return post_query.first()