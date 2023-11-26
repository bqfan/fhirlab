from fastapi import FastAPI, status, HTTPException, Depends
from typing import Final, List
from backend.src.utilities import resource_loader
# from pydantic import BaseModel, create_model
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.models.schemas.references import CodingItem, Code, High, Low, ReferenceRangeItem, Reference, Acronyms, TempEnum
# from . import models
# from .database import engine
# from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)

REFERENCES: Final[dict] = resource_loader.load_resources("default")

observation_keys_dict = {}
for key in REFERENCES["ObservationKeys"]:
    observation_keys_dict[key] = key

ObservationKeys = TempEnum("ObservationKeys", observation_keys_dict)

observation_keys_dict = {}
for key in REFERENCES["ObservationKeys"]:
    observation_keys_dict[key] = key

ReferenceKeys = TempEnum("ReferenceKeys", observation_keys_dict)

@app.get("/")
async def read_main():
    return {"msg": "LabTest API"}

@app.get("/v1/References")
def get_references() -> dict:
    return REFERENCES['Observations']

@app.get("/v1/References/keys")
def get_reference_by_id() -> list:
    return REFERENCES['ObservationKeys']

@app.get("/v1/References/{key}", response_model=Reference, response_model_exclude_unset=True)
def get_reference_by_id(key: ReferenceKeys):
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