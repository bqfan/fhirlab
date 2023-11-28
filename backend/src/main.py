from fastapi import FastAPI, status, HTTPException, Depends
from typing import Final, List

from fastapi.responses import RedirectResponse
from backend.src.api.resources.resource_loader import Resource
# from pydantic import BaseModel, create_model
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.models.schemas.references import CodingItem, Code, High, Low, ReferenceRangeItem, Reference, Bundle, Acronyms, TempEnum
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

resource = Resource().load()

reference_keys = {}
for key in resource.reference_keys:
    reference_keys[key] = key

ReferenceKeys = TempEnum("ReferenceKeys", reference_keys)

bundle_keys = {}
for key in resource.bundle_keys:
    bundle_keys[key] = key

BundleKeys = TempEnum("BundleKeys", bundle_keys)

acronym_keys = {}
for key in resource.acronyms["acronyms"]:
    acronym_keys[key] = key

AcronymKeys = TempEnum("BundleKeys", acronym_keys)


@app.get("/References")
def get_references() -> dict:
    return resource.references

@app.get("/References/keys")
def get_reference_keys() -> list:
    return resource.reference_keys

@app.get("/References/{key}", response_model=Reference, response_model_exclude_unset=True)
def get_reference_by_key(key: ReferenceKeys):
    try:
        reference = resource.references[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")

    return reference

@app.get("/References/{key}/referenceRange")
def get_reference_range_by_key(key: ReferenceKeys, response_model=List[ReferenceRangeItem], response_model_exclude_unset=True):
    try:
        referenceRange = resource.references[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange

@app.get("/References/{key}/code")
def get_reference_code_by_key(key: ReferenceKeys) -> Code:
    try:
        referenceCode = resource.references[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode

@app.get("/Bundles")
def get_bundles() -> dict:
    __bundle_formatter()

    return resource.bundles

@app.get("/Bundles/keys")
def get_bundle_keys() -> list:
    return resource.bundle_keys

@app.get("/Bundles/{key}", response_model=Bundle, response_model_exclude_unset=True)
def get_bundle_by_key(key: BundleKeys):
    __bundle_formatter()

    try:
        bundle = resource.bundles[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"bundle key {key} not found")

    return bundle

@app.get("/Acronyms")
def get_acronyms() -> dict:
    return resource.acronyms

@app.get("/Acronyms/{key}")
def get_reference_by_acronym(key: AcronymKeys):
    reference_key = resource.acronyms["acronyms"][key]

    return get_reference_by_key(reference_key)

def __bundle_formatter():
    for _, value in resource.bundles.items():
        for entry in value['entry']:
            entry['fullUrl'] = entry['fullUrl'].replace('BaseUrl', resource.base_url)
            if isinstance(entry['resource'], str):
                entry['resource'] = resource.references[entry['resource']]
