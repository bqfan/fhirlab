from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Final
from app.utils import reference_loader
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
REFERENCES: Final[dict] = reference_loader.load_references("default")

@app.get("/v1/References/")
def root() -> dict:
    return REFERENCES

@app.get("/v1/References/{resourceType}")
def root(resourceType: str) -> dict:
    return REFERENCES[resourceType]

# @app.get("/v1/References/keys")
# def keys() -> dict:
#     keys = list(REFERENCES.keys())
#     return keys

@app.get("/v1/References/{resourceType}/{key}")
def labvalue_by_key(resourceType: str, key: str) -> dict:
    try:
        labvalue = REFERENCES[resourceType][key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")
    return labvalue

# @app.get("/v1/References/{resourceType}/{key}/referenceRange")
# def labvalue_reference_range(resourceType, key) -> dict:
#     labvalue = labvalue_by_key(key)
#     try:
#         reference_range = labvalue["referenceRange"]
#     except KeyError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"referenceRange not found for lab value key {key}")
#     return reference_range

# @app.get("/v1/labvalues/{key}/referenceRange/high")
# def labvalue_reference_range_high(key) -> dict:
#     reference_range = labvalue_reference_range(key)
#     try:
#         high = reference_range["high"]
#     except KeyError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"referenceRange high not found for lab value key {key}")
#     return high
