
from __future__ import annotations
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Dict, Final, Union
from app.utils import reference_loader
from enum import Enum
from typing import Optional
# from pydantic import BaseModel, create_model
from typing import List
from pydantic import BaseModel
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

class CodingItem(BaseModel):
    code: str
    display: str
    system: str

class Code(BaseModel):
    coding: List[CodingItem]

class High(BaseModel):
    code: str
    system: str
    unit: str
    value: int

class Low(BaseModel):
    code: str
    system: str
    unit: str
    value: float

class ReferenceRangeItem(BaseModel):
    high: High
    low: Low

class Reference(BaseModel):
    resourceType: str
    code: Code
    referenceRange: List[ReferenceRangeItem]

class ResourceType(str, Enum):
    observation = "Observation"
    bundle = "Bundle"

class Acronyms(str, Enum):
    true = True
    false = False

class TempEnum(str, Enum):
    pass

observation_keys_dict = {}
for key in REFERENCES["ObservationKeys"]:
    observation_keys_dict[key] = key

observation_acronyms_keys_dict = {}
for key in REFERENCES["ObservationAcronymsKeys"]:
    observation_acronyms_keys_dict[key] = key

bundle_keys_dict = {}
for key in REFERENCES["BundleKeys"]:
    bundle_keys_dict[key] = key

bundle_acronyms_keys_dict = {}
for key in REFERENCES["BundleAcronymsKeys"]:
    bundle_acronyms_keys_dict[key] = key

ObservationKeys = TempEnum("ObservationKeys", observation_keys_dict | observation_acronyms_keys_dict)
ObservationAcronymKeys = TempEnum("ObservationAcronymKeys",  observation_acronyms_keys_dict)
BundleKeys = TempEnum("BundleKeys", bundle_keys_dict | bundle_acronyms_keys_dict)
ReferenceKeys = TempEnum("ReferenceKeys", observation_keys_dict | observation_acronyms_keys_dict | bundle_keys_dict | bundle_acronyms_keys_dict)

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

@app.get("/v1/References/keys")
def get_reference_by_id(resourceType: ResourceType | None = None, acronyms: Acronyms | None = None) -> list:
    if resourceType == "Observation" and acronyms == "True":
        keys = REFERENCES['ObservationAcronymsKeys']
    elif resourceType == "Observation" and acronyms == "False":
        keys = REFERENCES['ObservationKeys']
    elif resourceType == "Observation":
        keys = REFERENCES['ObservationKeys'] + REFERENCES['ObservationAcronymsKeys']
    elif resourceType == "Bundle" and acronyms == "True":
        keys = REFERENCES['BundleAcronymsKeys']
    elif resourceType == "Bundle" and acronyms == "False":
        keys = REFERENCES['BundleKeys']
    elif resourceType == "Bundle":
        keys = REFERENCES['BundleKeys'] + REFERENCES['BundleAcronymsKeys']
    elif acronyms == "True":
        keys = REFERENCES['ObservationAcronymsKeys'] + REFERENCES['BundleAcronymsKeys']
    elif acronyms == "False":
        keys = REFERENCES['ObservationKeys'] + REFERENCES['BundleKeys']
    else:
        keys = REFERENCES['ObservationKeys'] + REFERENCES['ObservationAcronymsKeys'] + REFERENCES['BundleKeys'] + REFERENCES['BundleAcronymsKeys'] 

    return keys

@app.get("/v1/References/{key}")
def get_reference_by_id(key: ReferenceKeys) -> Reference:
    try:
        reference = (REFERENCES["Observations"] | REFERENCES["ObservationAcronyms"] | REFERENCES["Bundles"] | REFERENCES["BundleAcronyms"])[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference id {key} not found")

    return reference

@app.get("/v1/References/{key}/code")
def get_reference_by_id(key: ObservationKeys) -> CodingItem:
    try:
        referenceCode = (REFERENCES["Observations"] | REFERENCES["ObservationAcronyms"])[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode

@app.get("/v1/References/acronyms/{key}/code/text")
def get_reference_by_id(key: ObservationAcronymKeys) -> CodingItem:
    try:
        referenceCodeText = REFERENCES["ObservationAcronyms"][key]["code"]["text"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCodeText

@app.get("/v1/References/{key}/referenceRange")
def get_reference_by_id(key: ObservationKeys) -> ReferenceRangeItem:
    try:
        referenceRange = (REFERENCES["Observations"] | REFERENCES["ObservationAcronyms"])[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange
