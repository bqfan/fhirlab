import enum
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Dict, Final
from app.utils import reference_loader
from enum import Enum
from typing import Optional
from pydantic import BaseModel, create_model

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

class ResourceType(str, Enum):
    observation = "Observation"
    bundle = "Bundle"

class TempEnum(str, Enum):
    pass

ObservationKeys = TempEnum("ObservationKeys", REFERENCES["Observation_keys"])
BundleKeys = TempEnum("BundleKeys", REFERENCES["Bundle_keys"])

@app.get("/v1/References/")
def root() -> dict:
    return REFERENCES

@app.get("/v1/References/{resourceType}")
def references_by_resource_type(resourceType: ResourceType) -> dict:
    try:
        references = REFERENCES[resourceType]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"resource type {resourceType} not found")
    return references

@app.get("/v1/References/Observation/{key}")
def observation_reference_by_key(key: ObservationKeys) -> dict:
    try:
        reference = REFERENCES["Observation"][key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")
    return reference

@app.get("/v1/References/Bundle/{key}")
def bundle_reference_by_key( key: BundleKeys) -> dict:
    try:
        reference = REFERENCES['Bundle'][key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")
    return reference
