
from __future__ import annotations
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Dict, Final, Union
from app.utils import reference_loader
from enum import Enum
from typing import Optional
# from pydantic import BaseModel, create_model
from typing import List
from pydantic import BaseModel, Field
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
    text: str

class High(BaseModel):
    code: str
    system: str
    unit: str
    value: float

class Low(BaseModel):
    code: str
    system: str
    unit: str
    value: float

class ReferenceRangeItem(BaseModel):
    low: Optional[Low] = None
    high: Optional[High] = None
    normalValue: List[str] = None
    type: List[str] = None
    appliesTo: List[List[str]] = None
    age: Optional[list[int]] = Field(None, ge=0, le=150, min_items=2, max_items=2, description="age", example=[50, 70])

class Reference(BaseModel):
    resourceType: str
    code: Code
    referenceRange: List[ReferenceRangeItem]

class Acronyms(str, Enum):
    true = True
    false = False

class TempEnum(str, Enum):
    pass

observation_keys_dict = {}
for key in REFERENCES["ObservationKeys"]:
    observation_keys_dict[key] = key

ObservationKeys = TempEnum("ObservationKeys", observation_keys_dict)

observation_keys_dict = {}
for key in REFERENCES["ObservationKeys"]:
    observation_keys_dict[key] = key

ReferenceKeys = TempEnum("ReferenceKeys", observation_keys_dict)

@app.get("/v1/References")
def get_references() -> dict:
    return REFERENCES['Observations']

@app.get("/v1/References/keys")
def get_reference_by_id() -> list:
    return REFERENCES['ObservationKeys']

@app.get("/v1/References/{key}")
def get_reference_by_id(key: ReferenceKeys) -> Reference:
    try:
        reference = (REFERENCES["Observations"])[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference id {key} not found")

    return reference


@app.get("/v1/References/{key}/referenceRange")
def get_reference_by_id(key: ObservationKeys) -> List[ReferenceRangeItem]:
    try:
        referenceRange = (REFERENCES["Observations"])[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange

@app.get("/v1/References/{key}/code")
def get_reference_by_id(key: ObservationKeys) -> Code:
    try:
        referenceCode = (REFERENCES["Observations"])[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode