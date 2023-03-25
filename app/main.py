import enum
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Dict, Final, Union
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

class Acronyms(str, Enum):
    true = True
    false = False

class TempEnum(str, Enum):
    pass

ObservationKeys = TempEnum("ObservationKeys", REFERENCES["ObservationKeys"] | REFERENCES["ObservationAcronymsKeys"])

# BundleKeys = TempEnum("BundleKeys", REFERENCES["Bundle_keys"])
ReferenceKeys = TempEnum("ReferenceKeys", REFERENCES["ObservationKeys"] | REFERENCES["ObservationAcronymsKeys"] | REFERENCES["BundleKeys"] | REFERENCES["BundleAcronymsKeys"])

@app.get("/v1/References")
def get_references(resourceType: ResourceType | None = None, acronyms: Acronyms | None = None) -> dict:
    if resourceType == "Observation" and acronyms == "True":
        references = REFERENCES['ObservationAcronyms']
    elif resourceType == "Observation" and acronyms == "False":
        references = REFERENCES['Observations']
    elif resourceType == "Bundle" and acronyms == "True":
        references = REFERENCES['BundleAcronyms']
    elif resourceType == "Bundle" and acronyms == "False":
        references = REFERENCES['Bundles']
    elif acronyms == "True":
        references = REFERENCES['ObservationAcronyms'] | REFERENCES['BundleAcronyms']
    elif acronyms == "False":
        references = REFERENCES['Observationss'] | REFERENCES['Bundles']
    elif resourceType == "Observation":
        references = REFERENCES['Observations'] | REFERENCES['ObservationAcronyms']
    elif resourceType == "Bundle":
        references = REFERENCES['Bundles'] | REFERENCES['BundleAcronyms']
    else:
        references = REFERENCES['Observations'] | REFERENCES['ObservationAcronyms'] | REFERENCES['Bundles'] | REFERENCES['BundleAcronyms'] 

    return references

@app.get("/v1/References/{id}")
def get_reference_by_id(id: ReferenceKeys) -> dict:
    try:
        reference = (REFERENCES["Observations"] | REFERENCES["ObservationAcronyms"] | REFERENCES["Bundles"] | REFERENCES["BundleAcronyms"])[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference id {id} not found")

    return reference

@app.get("/v1/References/{id}/code")
def get_reference_by_id(id: ObservationKeys) -> dict:
    try:
        referenceCode = (REFERENCES["Observations"] | REFERENCES["ObservationAcronyms"])[id]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with id {id} not found")

    return referenceCode

@app.get("/v1/References/{id}/referenceRange")
def get_reference_by_id(id: ObservationKeys) -> dict:
    try:
        referenceRange = (REFERENCES["Observations"] | REFERENCES["ObservationAcronyms"])[id]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with id {id} not found")

    return referenceRange
