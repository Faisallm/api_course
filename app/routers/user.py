from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import database, models, utils, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    # creating the hash of the user's password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        # when post is not found in our db.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id: {id} does not exist!.")
    
    return user








