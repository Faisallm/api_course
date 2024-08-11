from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, config
from .routers import post, user, auth, vote

# this is what create our models in the db.
# when you add alembic, you no longer need the line below
# but am just gonna leave it.
# it won't break anything.
models.Base.metadata.create_all(bind=database.engine)


# creating an instance of fastapi
app = FastAPI()

origins = ["*"]

# cors=cross origin resource sharing
# allows a website hosted on a different domain to talk to our
# server hosted on a different domain.

# a middleware is a function that runs before every request.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API!!!!"}


















