from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Final
from app.utils import labvalues_concatenator
# from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine
# from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)
LABVALUES: Final[dict] = labvalues_concatenator.concatenate("default")

@app.get("/v1/labvalues/")
def root():
    labvalues = labvalues_concatenator.concatenate("default")
    return labvalues

@app.get("/v1/labvalues/{id}")
def labvalue_by_id(id):
    global labvalues
    try:
        labvalue = LABVALUES[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"lab value: {id} does not exist")
    return labvalue

@app.get("/v1/labvalues/acronyms/{id}")
def labvalue_acronyms_by_id(id):
    labvalue = labvalues_concatenator.concatenate("default")["acronyms"][id]
    return labvalue